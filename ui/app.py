##TEST CONMBINATION##
from flask import Flask, render_template, jsonify
from user_db import User, validate_credentials
import json
import os
import mysql.connector
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout

app = Flask(__name__)
auth = HTTPBasicAuth()

es = Elasticsearch(["http://10.0.10.14:9200"])

users = {
    "admin": generate_password_hash("secret"),
    "user1": generate_password_hash("password1"),
}



@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@app.route('/')
def login_page():
    return render_template('Loginpage.html')

@app.route('/homepage')
def home():
    return render_template('app.html')


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
        return render_template('logs.html', honeypot=honeypot, logs=formatted_logs, headers=headers)
    except ConnectionError:
        print("Fail to connect to Elasticsearch")
        return "Fail to connect to Elasticsearch"
    except ConnectionTimeout:
        print("Fail to connect to Elasticsearch")
        return "Fail to connect to Elasticsearch"
    


@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/grafana')
def grafana():
    return render_template('grafana.html')

@app.route('/incoming-traffic')
@auth.login_required
def incoming_traffic():
    return render_template('incoming-traffic.html')


if __name__ == '__main__':
    app.run(debug=True)
