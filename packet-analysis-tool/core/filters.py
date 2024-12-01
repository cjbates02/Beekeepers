class PacketFilter:
    def filter_allow_ip_traffic(self, ip, direction):
        if direction == 'src':
            ips = self.allowed_src_ips
        else:
            ips = self.allowed_dst_ips
        
        if ips == []:
            return True
        
        for allowed_ip in ips:
            if allowed_ip == ip:
                return True
        
        return False

    
    
    def filter_allow_network_traffic(self, ip, direction):
        if direction == 'src':
            networks = self.allowed_src_networks
        else:
            networks = self.allowed_dst_networks 
        
        if networks == []:
            return True
        
        for allowed_network in networks:
            if ip in allowed_network:
                return True
        return False
    
    
    def filter_deny_ip_traffic(self, ip, direction):
        if direction == 'src':
            ips = self.denied_src_ips
        else:
            ips = self.denied_dst_ips
        
        if ips == []:
            return True
        
        for allowed_ip in ips:
            if allowed_ip == ip:
                return False
        return True

    
    
    def filter_deny_network_traffic(self, ip, direction):
        if direction == 'src':
            networks = self.denied_src_networks
        else:
            networks = self.denied_dst_networks 
        
        if networks == []:
            return True
        
        for denied_network in networks:
            if ip in denied_network:
                return False
        return True
    
    
    def apply_filters(self, ip, direction):
        ip = ipaddress.ip_address(ip)
        is_valid = self.filter_allow_ip_traffic(ip, direction)
        is_valid = self.filter_allow_network_traffic(ip, direction)
        return is_valid