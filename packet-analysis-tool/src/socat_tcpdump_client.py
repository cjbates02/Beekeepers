import socket
from scapy.all import Ether, IP, TCP, UDP, Raw  # type: ignore
import logging
import logging.config
import ipaddress
import struct
from packet_reassembler import PacketReassembler
from collections import deque


# TODO
# Add filters to show IP's from LAN or not
# Research packet analysis more, specifically how wireshark works
# How does this provide value?
# Connect to elasticsearch

# Filtering System

# Filter inbound traffic
# Filter outbound traffic
# Filter ports
# Filter IP addresses

class PacketSnifferClient:
    def __init__(self, # empty list means *
                 host, 
                 port, 
                 allowed_src_ips = [],
                 allowed_dst_ips = [],
                 allowed_src_networks = [],
                 allowed_dst_networks = [],
                 denied_src_ips = [],
                 denied_dst_ips = [],
                 denied_src_networks = [],
                 denied_dst_networks = [],
                 logging_config_file = ''):
        
        self.host = host
        self.port = port
        self.logging_config_file = logging_config_file
        self.allowed_src_ips = self.__format_ip_addresses(allowed_src_ips)
        self.allowed_dst_ips = self.__format_ip_addresses(allowed_dst_ips)
        self.allowed_src_networks = self.__format_network_addresses(allowed_src_networks)
        self.allowed_dst_networks  = self.__format_network_addresses(allowed_dst_networks)
        
        self.denied_src_ips = self.__format_ip_addresses(denied_src_ips)
        self.denied_dst_ips = self.__format_ip_addresses(denied_dst_ips)
        self.denied_src_networks = self.__format_network_addresses(denied_src_networks)
        self.denied_dst_networks  = self.__format_network_addresses(denied_dst_networks)
        self.reassembler = PacketReassembler()
        self.buffer = deque()

        if self.logging_config_file:
            logging.config.fileConfig(self.logging_config_file)


    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            while True:
                data = s.recv(4096)
                if data:
                    self.process_raw_data(data)
                else:
                    logging.warning('Did not recieve any data from the server')
                    break


    def __format_ip_addresses(self, ips):
        return [ipaddress.ip_address(ip) for ip in ips]  
    
    
    def __format_network_addresses(self, networks):
        return [ipaddress.ip_network(network) for network in networks]  



    # def process_raw_data(self, data):
    #     try:
    #         self.buffer.append(data)
    #         while len(self.buffer) > 0:
    #             current_data = b''.join(self.buffer)
    #             if len(current_data) < 14:
    #                 break
    #             try:
    #                 packet = Ether(current_data)
    #                 #self.__get_src_and_dst(packet)
                    
    #                 full_packet = self.reassembler.add_fragment(packet)

    #                 if full_packet:
    #                     self.get_src_and_dst_addr(full_packet)

    #                 processed_length = len(packet)  
    #                 current_data = current_data[processed_length:]
    #                 self.buffer = deque([current_data]) if current_data else deque()

    #             except Exception as e:
    #                 logging.warning('Error processing packet: %s', e)
    #                 self.buffer.popleft()  # Remove the first incomplete packet
                        
    #     except struct.error as e:
    #         print(e)
    #         print(data)
    #         logging.warning('Recieved a packet that was not 2 bytes.')
        
        
        
    def process_raw_data(self, data):
        try:
            packet = Ether(data)
            if not packet.haslayer(IP):
                return
            ip_layer = packet[IP]
            #print(ip_layer.flags.MF, ip_layer.frag, packet.summary())
            logging.info(f'Source IP: {ip_layer.src} Destination IP: {ip_layer.dst}')
            
        except struct.error as e:
            logging.warning('Recieved a packet that was not 2 bytes. Attempting to reassemble...')
            if not packet.haslayer(IP):
                return
            full_packet = self.reassembler.add_fragment(packet)
            if full_packet:
                ip_layer = full_packet[IP]
                logging.info(f'Source IP: {ip_layer.src} Destination IP: {ip_layer.dst}')
            
        
    
    def get_src_and_dst_addr(self, packet):
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            honeypot_ips = [ipaddress.ip_address('10.0.10.10'), ipaddress.ip_address('10.0.10.11')]
            #if self.apply_filters(src_ip, 'src') and self.apply_filters(dst_ip, 'dst'):
            # if ipaddress.ip_address(dst_ip) in honeypot_ips:
            logging.info(f'Source IP: {src_ip} Destination IP: {dst_ip}')





if __name__ == '__main__':
    HOST = '10.0.10.13'
    PORT = 6000
    INBOUND_NETWORK_EXCLUSIONS = [ # optional
            '10.0.10.0/24',
            '10.0.197.0/24',
            '10.0.97.0/24'
        ]

    # client = PacketSnifferClient(host=HOST, 
    #                              port=PORT, 
    #                              inbound_networks=INBOUND_NETWORK_EXCLUSIONS)
    client = PacketSnifferClient(host=HOST, 
                                 port=PORT, 
                                 logging_config_file='../logging.ini',
                                 )
    
    
    
    client.start_client()

