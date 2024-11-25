##TEST CONMBINATION##
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from core import user_db
import uuid
import json
import os
import mysql.connector
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout
from prometheus_api_client import PrometheusConnect

app = Flask(__name__)
app.secret_key = 'beekeepers'
auth = HTTPBasicAuth()

# Initialize Prometheus and Elasticsearch connections
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
es = Elasticsearch(["http://10.0.10.14:9200"])

users = {
    "admin": generate_password_hash("secret"),
    "user1": generate_password_hash("password1"),
}

def check_authentication():
    if session.get('uid', None):
        return True
    return False

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
        # If valid, redirect to the homepage
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login_page'))
    
@app.route('/create-account')
def create():
    if check_authentication():
        return render_template('createacc.html')
    flash('User not authenticated')
    return redirect(url_for('login_page'))

@app.route('/homepage')
def home():
    if check_authentication():
        return render_template('app.html')
    flash('User not authenticated')
    return redirect(url_for('login_page'))
    


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
        print(headers)
        if check_authentication():
            return render_template('logs.html', honeypot=honeypot, logs=formatted_logs, headers=headers)
        flash('User not authenticated')
        return redirect(url_for('login_page'))
        
        
    except ConnectionError:
        print("Fail to connect to Elasticsearch")
        return "Fail to connect to Elasticsearch"
    except ConnectionTimeout:
        print("Fail to connect to Elasticsearch")
        return "Fail to connect to Elasticsearch"
    


@app.route('/alerts')
def alerts():
    if check_authentication():
        return render_template('alerts.html')
    flash('User not authenticated')
    return redirect(url_for('login_page'))

@app.route('/status')
def grafana():
    if check_authentication():
        return render_template('status.html')
    flash('User not authenticated')
    return redirect(url_for('login_page'))

@app.route('/incoming-traffic')
def incoming_traffic():
    if check_authentication():
        return render_template('incoming-traffic.html')
    flash('User not authenticated')
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/homepage')
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
