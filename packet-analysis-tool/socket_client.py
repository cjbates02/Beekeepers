import socket

HOST = '10.0.10.13'
PORT = 6000



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(4096)

print('Recieved', data)