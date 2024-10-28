import sys
import pytest

sys.path.append('../src')

from src.socat_tcpdump_client import PacketSnifferClient

class TestPacketSnifferClient:
    def setup_method(self):
        HOST, PORT = '0.0.0.0', 00000
        self.packet_sniffer_client = PacketSnifferClient(HOST, PORT)
        
    
    def test_ip_filter(self):
        assert self.packet_sniffer_client.filter_ip_traffic('1.1.1.1', 'src') == True
        assert self.packet_sniffer_client.filter_ip_traffic('1.1.1.1', 'dst') == True
        self.packet_sniffer_client.allowed_inbound_ips = ['10.0.10.100']
        assert self.packet_sniffer_client.filter_ip_traffic('1.1.1.1', 'src') == False
        assert self.packet_sniffer_client.filter_ip_traffic('10.0.10.100', 'src') == True
        assert self.packet_sniffer_client.filter_ip_traffic('1.1.1.1', 'dst') == True
        
        
        

