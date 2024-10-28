import socket
from scapy.all import Ether, IP, TCP, UDP, Raw  # type: ignore
import logging
import logging.config
import ipaddress
import struct


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
                 allowed_inbound_ips = [],
                 allowed_outbound_ips = [],
                 allowed_inbound_networks = [],
                 allowed_outbound_networks = [],
                 logging_config_file = ''):
        
        self.host = host
        self.port = port
        self.logging_config_file = logging_config_file
        self.allowed_inbound_ips = self.__format_ip_addresses(allowed_inbound_ips)
        self.allowed_outbound_ips = self.__format_ip_addresses(allowed_outbound_ips)
        self.allowed_inbound_networks = self.__format_network_addresses(allowed_inbound_networks)
        self.allowed_outbound_networks = self.__format_network_addresses(allowed_outbound_networks)

        if self.logging_config_file:
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
                    break


    def __format_ip_addresses(self, ips):
        return [ipaddress.ip_address(ip) for ip in ips]  
    
    
    def __format_network_addresses(self, networks):
        return [ipaddress.ip_network(network) for network in networks]  


    def filter_ip_traffic(self, ip, direction):
        if direction == 'src':
            ips = self.allowed_inbound_ips
        else:
            ips = self.allowed_outbound_ips
        
        if ips == []:
            return True
        
        for allowed_ip in ips:
            if allowed_ip == ip:
                return True
        return False
    
    
    def filter_network_traffic(self, ip, direction):
        if direction == 'src':
            networks = self.allowed_inbound_networks
        else:
            networks = self.allowed_outbound_networks
        
        if networks == []:
            return True
        
        for allowed_network in networks:
            if ip in allowed_network:
                return True
        return False
    
    
    def apply_filters(self, ip, direction):
        ip = ipaddress.ip_address(ip)
        is_valid = self.filter_ip_traffic(ip, direction)
        is_valid = self.filter_network_traffic(ip, direction)
        return is_valid


    def __process_raw_data(self, data):
        try:
            packet = Ether(data)
            self.__get_src_and_dst(packet)
        except struct.error as e:
            logging.warning('Recieved a packet that was not 2 bytes.')
        
    
    def __get_src_and_dst(self, packet):
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst

            if self.apply_filters(src_ip, 'src') and self.apply_filters(dst_ip, 'dst'):
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
    client = PacketSnifferClient(host=HOST, port=PORT, logging_config_file='../logging.ini')
    
    
    
    client.start_client()

