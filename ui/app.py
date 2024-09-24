from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/grafana')
def grafana():
    return render_template('grafana.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/incoming-traffic')
def incoming_traffic():
    return render_template('incoming-traffic.html')

@app.route('/login')
def login_page():
    return render_template('Loginpage.html')

if __name__ == '__main__':
    app.run(debug=True)


