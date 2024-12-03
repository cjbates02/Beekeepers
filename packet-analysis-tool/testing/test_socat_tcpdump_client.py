import sys
import pytest
import ipaddress

sys.path.append('../src')

from src.socat_tcpdump_client import PacketSnifferClient

class TestPacketSnifferClient:
    def setup_method(self):
        HOST, PORT = '0.0.0.0', 00000
        self.packet_sniffer_client = PacketSnifferClient(HOST, PORT)
        
    
    # def test_allow_ip_filter(self):
    #     assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'src') == True
    #     assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'dst') == True
    #     self.packet_sniffer_client.allowed_src_ips = ['10.0.10.100']
    #     assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'src') == False
    #     assert self.packet_sniffer_client.filter_allow_ip_traffic('10.0.10.100', 'src') == True
    #     assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'dst') == True
        
    
    # def test_deny_ip_filter(self):
    #     assert self.packet_sniffer_client.filter_deny_ip_traffic('1.1.1.1', 'src') == True
    #     assert self.packet_sniffer_client.filter_deny_ip_traffic('1.1.1.1', 'dst') == True
    #     self.packet_sniffer_client.denied_src_ips = ['10.0.10.100']
    #     assert self.packet_sniffer_client.filter_deny_ip_traffic('10.0.10.100', 'src') == False
    #     assert self.packet_sniffer_client.filter_deny_ip_traffic('1.1.1.1', 'src') == True
        
    def test_allow_ip_filter(self):
        # Test with IP not in allowed list (initial state)
        assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'src') == True
        assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'dst') == True

        # Update allowed source and destination IPs
        self.packet_sniffer_client.allowed_src_ips = ['10.0.10.100']
        self.packet_sniffer_client.allowed_dst_ips = ['20.0.10.200']
        
        # Check with an IP that is not allowed
        assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'src') == False  # Not allowed
        assert self.packet_sniffer_client.filter_allow_ip_traffic('10.0.10.100', 'src') == True  # Allowed
        assert self.packet_sniffer_client.filter_allow_ip_traffic('1.1.1.1', 'dst') == False  # Not allowed
        assert self.packet_sniffer_client.filter_allow_ip_traffic('20.0.10.200', 'dst') == True  # Allowed

        # Test with a destination IP that is not allowed
        assert self.packet_sniffer_client.filter_allow_ip_traffic('30.0.0.1', 'dst') == False  # Not allowed
        self.packet_sniffer_client.allowed_dst_ips.append('30.0.0.1')
        assert self.packet_sniffer_client.filter_allow_ip_traffic('30.0.0.1', 'dst') == True  # Now allowed


    def test_filter_allow_network_traffic(self):
        # Setup: Initialize the allowed networks
        self.packet_sniffer_client.allowed_src_networks = ['10.0.0.0/24']
        self.packet_sniffer_client.allowed_dst_networks = ['192.168.1.0/24']

        # Test source direction with IPs in the allowed source network
        assert self.packet_sniffer_client.filter_allow_network_traffic('10.0.0.15', 'src') == True
        assert self.packet_sniffer_client.filter_allow_network_traffic('10.0.0.1', 'src') == True

        # Test source direction with IPs not in the allowed source network
        assert self.packet_sniffer_client.filter_allow_network_traffic('10.1.0.15', 'src') == False
        assert self.packet_sniffer_client.filter_allow_network_traffic('192.168.1.10', 'src') == False

        # Test destination direction with IPs in the allowed destination network
        assert self.packet_sniffer_client.filter_allow_network_traffic('192.168.1.15', 'dst') == True
        assert self.packet_sniffer_client.filter_allow_network_traffic('192.168.1.1', 'dst') == True

        # Test destination direction with IPs not in the allowed destination network
        assert self.packet_sniffer_client.filter_allow_network_traffic('192.168.2.15', 'dst') == False
        assert self.packet_sniffer_client.filter_allow_network_traffic('10.0.0.10', 'dst') == False

        # Edge case: Check when allowed networks are empty
        self.packet_sniffer_client.allowed_src_networks = []
        self.packet_sniffer_client.allowed_dst_networks = []
        assert self.packet_sniffer_client.filter_allow_network_traffic('10.0.0.15', 'src') == True  # Allowed
        assert self.packet_sniffer_client.filter_allow_network_traffic('192.168.1.15', 'dst') == True  # Allowed



        
        

