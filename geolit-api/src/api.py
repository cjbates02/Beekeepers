from flask import Flask, send_file

app = Flask(__name__)

@app.route('/geolite2', methods=['GET'])
def send_geolite_file():
    return send_file('./GeoLite2-ASN.mmdb', as_attachment=True)

if __name__ == '__main__':
    app.run()
