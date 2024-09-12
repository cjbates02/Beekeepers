from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/alerts')
def alers():
    return render_template('app.html')

@app.route('/grafana')
def grafana():
    return render_template('app.html')

@app.route('/logs')
def logs():
    return render_template('app.html')

@app.route('/incoming_traffic')
def incoming_traffic():
    return render_template('app.html')

@app.route('/login')
def login_page():
    return render_template('Loginpage.html')

if __name__ == '__main__':
    app.run(debug=True)


