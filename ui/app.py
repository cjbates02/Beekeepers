##TEST CONMBINATION##
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from flask_socketio import SocketIO
from core import user_db, prom_client
import uuid
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout
import logging
import sys
import time
import queue
import threading

logger = logging.getLogger('FlaskLogger')
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = 'beekeepers'
auth = HTTPBasicAuth()
socket = SocketIO(app, cors_allowed_origins="*")

es = Elasticsearch(["http://10.0.10.14:9200"])
prom = prom_client.PromClient()

prom_data_queue = queue.Queue()

users = {
    "admin": generate_password_hash("secret"),
    "user1": generate_password_hash("password1"),
}

def check_authentication():
    session.pop('_flashes', None)
    if session.get('uid', None):
        return True
    flash('User not authenticated')
    return False


def broadcast_prom_data():
    while True:
        if not prom_data_queue.empty():
            broadcast_data = prom_data_queue.get()
            socket.emit('prom_data', {'data': broadcast_data})
            logger.info('Broadcasted data to all clients.')
        time.sleep(15)


def retrieve_prom_data():
    while True:
        data = prom.main()
        prom_data_queue.put(data)
        time.sleep(10)


def does_thread_exist(thread_name):
    if any(thread.name == thread_name for thread in threading.enumerate()):
        return True
    else:
        return False


def start_thread(target, name):
    logger.info(f'Creating {name} thread.')
    threading.Thread(target=target, name=name, daemon=True).start()


@socket.on('connect')
def handle_connect():
    logger.info(f'Client has connected to socket with sid {request.sid}')
    if not does_thread_exist('broadcast_prom_data'):
        start_thread(broadcast_prom_data, 'broadcast_prom_data')
        
    if not does_thread_exist('retrieve_prom_data'):
        start_thread(retrieve_prom_data, 'retrieve_prom_data')


@app.route('/')  # Starts at Login Page
def login_page():
    return render_template('Loginpage.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    unhashed_password = request.form.get('password')
    user = user_db.User(username, unhashed_password)

    if user.validate_credentials(username, unhashed_password):
        session['uid'] = uuid.uuid4()
        session['username'] = username
        # If valid, redirect to the homepage
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login_page'))


@app.route('/create-account', methods=['GET', 'POST'])
def create():
    if check_authentication():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = user_db.User(username, password)
            user.create_user()
            return redirect(url_for('home'))
        if session['username'] == 'admin':
            return render_template('createacc.html')
        
        flash('User does not have permssion for this page')

    return redirect(url_for('login_page'))


# @app.route('/homepage')
# def home():
#     if check_authentication():
#         return render_template('app.html')
#     flash('User not authenticated')
#     return redirect(url_for('login_page'))
    


@app.route('/logs/<honeypot>')
def logs(honeypot):
    try:
        response = es.search(
            index=f"{honeypot}-logs-new-*",  
            body={
                "query": {"match_all": {}},
                "sort": [{"@timestamp": {"order": "desc"}}],
                "size": 100
            }
        )
        logs_data = response['hits']['hits'][::-1]
        formatted_logs = [log['_source'] for log in logs_data]
        headers = formatted_logs[0].keys()
        if check_authentication():
            return render_template('logs.html', honeypot=honeypot, logs=formatted_logs, headers=headers)
        return redirect(url_for('login_page'))
    except ConnectionError:
        logger.error("Fail to connect to Elasticsearch")
        return "Fail to connect to Elasticsearch"
    except ConnectionTimeout:
        logger.error("Fail to connect to Elasticsearch")
        return "Fail to connect to Elasticsearch"
    

@app.route('/alerts')
def alerts():
    if check_authentication():
        return render_template('alerts.html')
    return redirect(url_for('login_page'))

@app.route('/status')
def grafana():
    if check_authentication():
        return render_template('status.html')
    return redirect(url_for('login_page'))

@app.route('/incoming-traffic')
def incoming_traffic():
    if check_authentication():
        return render_template('incoming-traffic.html')
    flash('User not authenticated')
    return redirect(url_for('login_page'))


@app.route('/homepage', methods=['GET', 'POST'])
def home():
    if check_authentication():
        # Sample data to be replaced with real metrics from Prometheus or Elasticsearch
        honeypots = [
            {"name": "Honeypot 1", "metric": 85},
            {"name": "Honeypot 2", "metric": 120},
            {"name": "Honeypot 3", "metric": 60},
            {"name": "Honeypot 4", "metric": 200},
            {"name": "Honeypot 5", "metric": 45},
        ]
        return render_template('app.html', honeypots=honeypots)
    flash('User not authenticated')
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5050, allow_unsafe_werkzeug=True)
    