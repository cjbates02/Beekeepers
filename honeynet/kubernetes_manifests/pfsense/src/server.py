from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = ''
PORT_NUMBER = 8000

class pfSenseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle static files
        if self.path.endswith('.html'):
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
        self.send_response(200)
        self.end_headers()
        


def run(server_class=HTTPServer, handler_class=pfSenseHandler):
    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    try:
        print('pfSense Honeytpot Started')
        run()
    except KeyboardInterrupt:
        print('Bye bye...')