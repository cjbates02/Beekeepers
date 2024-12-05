import socket
from scapy.all import Ether, IP, TCP, wrpcap
import logging
import logging.config
import ipaddress
import struct
import logging
import sys
import base64


# TODO
# Tag an ip address
# View metrics for a particular ip address
# View payload for a particular ip address
# Export payload of a packet into pcap file
# Export raw ip address data
# Retention policy (24 hours by default)
# Pause sniffer

class PacketSnifferClient:
    def __init__(self, host, port, logger):
        self.host = host
        self.port = port
        self.logger = logger


    def start_client(self) -> any:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.logger.info(f'Socat host: {self.host}, Socat port: {self.port}')
            self.logger.info('Attempting to connect to socat server.')
            s.connect((self.host, self.port))
            self.logger.info('Connected to socat server.')
            while True:
                data = s.recv(4096)
                if data:
                    packet_obj = self.process_raw_data(data)
                    yield packet_obj
                else:
                    self.logger.warning('Did not recieve any data from the server')
                    break 
        
        
    def process_raw_data(self, data) -> dict:
        ip_src, ip_dst, port_src, port_dst = None, None, None, None
        packet_obj = {}
        try:
            packet = Ether(data)
            if packet.haslayer(IP):
                ip_layer = packet[IP]
                ip_src, ip_dst = ip_layer.src, ip_layer.dst
                # self.logger.info(f'Source IP: {ip_src} Destination IP: {ip_dst}')
            if packet.haslayer(TCP):
                tcp_layer = packet[TCP]
                port_src, port_dst = tcp_layer.sport, tcp_layer.dport
                # self.logger.info(f'Source Port: {port_src} Destination Port: {port_dst}')
            if packet.haslayer(IP) or packet.haslayer(TCP):
                packet_obj = self.create_packet_object(ip_src, ip_dst, port_src, port_dst, data)
        except struct.error as e:
            self.logger.warning('Unable to decode packet.')
        finally:
            return packet_obj
            
    
    def create_packet_object(self, ip_src=None, ip_dst=None, port_src=None, port_dst=None, packet=None) -> dict:
        base64packet = self.encode_packet(packet)
        return {'ip_src': ip_src, 'ip_dst': ip_dst, 'port_src': port_src, 'port_dst': port_dst, 'base64packet': base64packet}
    
    
    def encode_packet(self, packet): 
        encoded_packet = base64.b64encode(packet).decode('utf-8')
        return encoded_packet
    
    
    def decode_packet(self, base64packet):
        decoded_packet = base64.b64decode(base64packet)
        return decoded_packet

    
    def generate_pcap_file(self, packets):
        packets = [Ether(self.decode_packet(packet)) for packet in packets]
        wrpcap('temp/capture.pcap', packets)


if __name__ == '__main__':
    HOST = '10.0.10.13'
    PORT = 6000
    logging.basicConfig(
        stream=sys.stdout,      
        level=logging.DEBUG,     
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' 
    )
    logger = logging.getLogger(__name__)
    client = PacketSnifferClient(host=HOST, port=PORT, logger=logger)
    client.start_client()

