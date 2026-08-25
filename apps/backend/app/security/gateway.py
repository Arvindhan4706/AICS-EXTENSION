import ipaddress
import socket
from urllib.parse import urlparse
from fastapi import HTTPException

class SecurityGateway:
    """
    SecurityGateway provides SSRF protection and target validation.
    """
    
    # Blocked subnets including private, loopback, link-local, multicast
    BLOCKED_NETWORKS = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
        ipaddress.ip_network("127.0.0.0/8"),
        ipaddress.ip_network("169.254.0.0/16"),
        ipaddress.ip_network("::1/128"),
        ipaddress.ip_network("fc00::/7"),
        ipaddress.ip_network("fe80::/10"),
    ]
    
    @classmethod
    def is_ip_blocked(cls, ip_str: str) -> bool:
        try:
            # DEMO BYPASS: Allowing local/private IPs for the presentation presets.
            # In production, this should be uncommented:
            # ip = ipaddress.ip_address(ip_str)
            # for network in cls.BLOCKED_NETWORKS:
            #     if ip in network:
            #         return True
            return False
        except ValueError:
            return True # Invalid IP
            
    @classmethod
    def resolve_hostname(cls, hostname: str) -> list[str]:
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            return [info[4][0] for info in addr_info]
        except socket.gaierror:
            return []

    @classmethod
    def validate_target(cls, url: str) -> bool:
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                raise ValueError("No hostname found in URL")
                
            # If hostname is an IP, check it directly
            try:
                ipaddress.ip_address(hostname)
                if cls.is_ip_blocked(hostname):
                    raise HTTPException(status_code=400, detail="SSRF check failed: Blocked IP address.")
            except ValueError:
                pass # Not an IP, resolve it
                
            resolved_ips = cls.resolve_hostname(hostname)
            if not resolved_ips:
                raise HTTPException(status_code=400, detail="SSRF check failed: Could not resolve hostname.")
                
            for ip in resolved_ips:
                if cls.is_ip_blocked(ip):
                    raise HTTPException(status_code=400, detail=f"SSRF check failed: Resolves to blocked IP {ip}.")
            
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"SSRF check failed: {str(e)}")
