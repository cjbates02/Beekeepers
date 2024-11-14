##TEST CONMBINATION##
from prometheus_api_client import PrometheusConnect
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from user_db import User, validate_credentials
import json
import os
import mysql.connector
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout

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

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@app.route('/')  # Starts at Login Page
def login_page():
    return render_template('Loginpage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if verify_password(username, password):
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login_page'))

@app.route('/homepage')
def home():
    return render_template('app.html')

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
        return render_template('logs.html', honeypot=honeypot, logs=formatted_logs, headers=headers)
    except (ConnectionError, ConnectionTimeout):
        return "Failed to connect to Elasticsearch"

@app.route('/metrics')
def get_metrics():
    # Define a list of Prometheus metric queries
    metric_queries = {
        "cpu_usage": 'container_cpu_usage_seconds_total',
        "memory_usage": 'container_memory_usage_bytes',
        "network_receive": 'container_network_receive_bytes_total',
        "network_transmit": 'container_network_transmit_bytes_total'
    }

    pod_metrics = {}

    # Loop through each metric query and retrieve data from Prometheus
    for metric_name, query in metric_queries.items():
        data = prom.custom_query(query=query)

        for item in data:
            pod_name = item['metric'].get('pod', 'unknown_pod')  # Get pod name
            value = item['value'][1]  # Metric value

            # Initialize pod entry if not present
            if pod_name not in pod_metrics:
                pod_metrics[pod_name] = {}

            # Add the metric to the pod's dictionary
            pod_metrics[pod_name][metric_name] = value

    return jsonify(pod_metrics)

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/status')
def grafana():
    return render_template('status.html')

@app.route('/incoming-traffic')
def incoming_traffic():
    return render_template('incoming-traffic.html')

if __name__ == '__main__':
    app.run(debug=True)
