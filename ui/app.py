from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/logs')
def logs():
    # Get the absolute path to the JSON file
    file_path = os.path.join(os.path.dirname(__file__), 'test_data.json')

    try:
         with open(file_path, 'r') as file:
            logs_data = json.load(file)
    except FileNotFoundError:
        logs_data = []  # In case the file is not found, return an empty list

    # Pass the logs to the logs.html template
    return render_template('logs.html', logs=logs_data)

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/grafana')
def grafana():
    return render_template('grafana.html')

@app.route('/incoming-traffic')
def incoming_traffic():
    return render_template('incoming-traffic.html')

@app.route('/login')
def login_page():
    return render_template('Loginpage.html')

if __name__ == '__main__':
    app.run(debug=True)

