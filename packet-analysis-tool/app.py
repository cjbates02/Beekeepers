import logging
import sys
import threading

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from core import client
from diskcache import Cache
from dotenv import load_dotenv
from os import getenv

load_dotenv()
SOCAT_HOST = getenv('SOCAT_HOST')
SOCAT_PORT =  int(getenv('SOCAT_PORT'))

logging.basicConfig(
        stream=sys.stdout,      
        level=logging.DEBUG,     
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' 
    )

logger = logging.getLogger('packet_sniffer')
packet_cache = Cache('packet_cache')

socat_client = client.PacketSnifferClient(SOCAT_HOST, SOCAT_PORT, logger)

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")


def broadcast_packet_data():
    packet_generator = socat_client.start_client()
    for packet in packet_generator:
        if packet:
            socket_io.emit('packet', {'packet': packet})


def does_thread_exist(thread_name):
    if any(thread.name == thread_name for thread in threading.enumerate()):
        return True
    else:
        return False


def start_thread(target, name):
    if not does_thread_exist(name):
        logger.info(f'Creating {name} thread.')
        threading.Thread(target=target, name=name, daemon=True).start()


# def add_packet_to_cache(packet):
#     with Cache(packet_cache.directory) as reference:
#         reference.set('', 'value')


@socket_io.on('connect')
def handle_socket_connect():
    logger.info(f'Client has connected to socket with sid {request.sid}')
    if not does_thread_exist('broadcast_prom_data'):
        start_thread(broadcast_packet_data, 'broadcast_packet_data')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socket_io.run(app, debug=True)

    