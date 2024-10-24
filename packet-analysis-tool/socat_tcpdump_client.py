import socket
from scapy.all import Ether, IP, TCP, UDP, Raw
import logging
import logging.config


class PacketSnifferClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logging_config_file = 'logging.ini'
        logging.config.fileConfig(self.logging_config_file)


    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            while True:
                data = s.recv(4096)
                if data:
                    self.__process_raw_data(data)
                else:
                    logging.warning('Did not recieve any data from the server')


    def __process_raw_data(self, data):
        packet = Ether(data)
        self.__get_src_and_dst(packet)
        #logging.info(packet.summary())
    
    
    def __get_src_and_dst(self, packet):
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            logging.info(f'Source IP: {src_ip}, Destination IP: {dst_ip}')


    



if __name__ == '__main__':
    HOST = '10.0.10.13'
    PORT = 6000

    client = PacketSnifferClient(HOST, PORT)
    client.start_client()

