from flask import Flask, jsonify
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

# Protected route
@app.route('/protected')
@auth.login_required
def protected():
    return jsonify({"message": f"Hello, {auth.current_user()}! This is a protected route."})

@app.route('/')
def public():
    return jsonify({"message": "Welcome to the public route!"})

if __name__ == '__main__':
    app.run(debug=True)

 
