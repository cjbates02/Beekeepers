from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import datetime

HOST_NAME = ''
PORT_NUMBER = 8000

class pfSenseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle static files
        if self.path == f'{HOST_NAME}/' or self.path == f'{HOST_NAME}/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html') as f:
                self.wfile.write(f.read().encode())
        elif self.path == f'{HOST_NAME}/login.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html') as f:
                self.wfile.write(f.read().encode())
        elif self.path.endswith('.jpg') or self.path.endswith('.png'):
            try:
                with open(self.path[1:], 'rb') as f:  # remove leading '/'
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg' if self.path.endswith('.jpg') else 'image/png')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")

        else:
            self.send_error(404, "File not found")


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode())
        
        # Log the data
        with open('./logs/log.txt', 'a') as log_file:
            username = parsed_data.get('username', [''])[0]
            password = parsed_data.get('password', [''])[0]
            ip = self.client_address[0]
            log_file.write(f"Time: {datetime.datetime.now()}, Username: {username}, Password: {password}, IP: {ip}\n")
        
        # Send a response
        self.send_response(302)
        self.send_header('Location', 'login.html')
        self.end_headers()



def run(server_class=HTTPServer, handler_class=pfSenseHandler):
    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    try:
        print('pfSense Honeypot Started')
        run()
    except KeyboardInterrupt:
        print('Bye bye...')