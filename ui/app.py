##TEST CONMBINATION##
from flask import Flask, render_template, jsonify
import json
import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

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


@app.route('/logs')
def logs():
    # Get the absolute path to the JSON file
    file_path = os.path.join(os.path.dirname(__file__), 'test_data.json')
    print(file_path)

    with open(file_path, 'r') as file:
        logs_data = json.load(file)
    print(logs_data)

    # Pass the logs to the logs.html template
    return render_template('logs.html', logs=logs_data['logs'])

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
