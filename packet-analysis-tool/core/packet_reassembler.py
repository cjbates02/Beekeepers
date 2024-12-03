from collections import defaultdict
from scapy.all import IP

class PacketReassembler:
    def __init__(self):
        self.fragments = defaultdict(list)
        self.original_packet_lengths = {}
    
    
    def add_fragment(self, packet):
        ip_layer = packet[IP]
        if ip_layer.frag > 0 or ip_layer.flags.MF:
            key = (ip_layer.src, ip_layer.id)
            if key not in self.original_packet_lengths:
                self.original_packet_lengths[key] = ip_layer.len
            self.fragments[key].append(packet)
            
        
            if self.is_complete(key):
                full_packet = self.reassemble(key)
                del self.fragments[key]
                return full_packet
            return None
        else:
            return packet
    
    
    def is_complete(self, key):
        if len(self.fragments[key]) == self.get_expected_length(key):
            return True
        return False
    
    
    def get_expected_length(self, key):
        original_length = self.original_packet_lengths.get(key)
        if original_length == None:
            return 0
        mtu = 1480
        return (original_length + mtu - 1) // mtu
    
    
    def reassemble(self, key):
        fragments = self.fragments[key]
        #fragments.sort(key=lambda pkt: pkt[IP].frag)
        full_payload = b''.join([bytes(frag) for frag in fragments])
        return IP(full_payload)
    
        
            
        
        