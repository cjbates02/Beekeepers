##TEST CONMBINATION##
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from user_db import User
import uuid
import json
import os
import mysql.connector
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout

app = Flask(__name__)
app.secret_key = 'beekeepers'
auth = HTTPBasicAuth()

es = Elasticsearch(["http://10.0.10.14:9200"])

users = {
    "admin": generate_password_hash("secret"),
    "user1": generate_password_hash("password1"),
}

def check_authentication():
    if session.get('uid', None):
        return True
    return False

@app.route('/')  #Starts at Login Page
def login_page():
    return render_template('Loginpage.html')

@app.route('/login', methods=['POST'])
def login():
    # Retrieve username and password from the submitted form
    username = request.form.get('username')
    unhashed_password = request.form.get('password')
    user = User(username, unhashed_password)

    if user.validate_credentials(username, unhashed_password):
        session['uid'] = uuid.uuid4()
        # If valid, redirect to the homepage
        return redirect(url_for('home'))
    else:
        # If invalid, show a flash message and redirect back to login page
        flash('Invalid username or password. Please try again.')
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
                "query": {
                    "match_all": {}  
                },
                "sort": [
                    {"@timestamp": {"order": "desc"}}
                ],
                "size": 100
            }
        )
        logs_data = response['hits']['hits']
        logs_data = logs_data[::-1]
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


