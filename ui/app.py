##TEST CONMBINATION##
from flask import Flask, render_template, jsonify
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
def home():
    return render_template('app.html')


@app.route('/logs/<honeypot>')
def logs(honeypot):
    try:
        response = es.search(
            index=f"{honeypot}-logs-*",  # Assuming your logs are in 'logs-index'
            body={
                "query": {
                    "match_all": {}  # Adjust this to fetch specific logs, filters can be applied here
                }
            }
        )
        logs_data = response['hits']['hits']
        formatted_logs = [log['_source'] for log in logs_data]

        return render_template('logs.html', logs=formatted_logs)
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

@app.route('/login')
def login_page():
    return render_template('Loginpage.html')

if __name__ == '__main__':
    app.run(debug=True)
