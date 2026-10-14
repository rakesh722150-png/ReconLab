import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore


class PortScanner:
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
                    443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432,
                    5900, 8080, 8443, 8888, 27017]
    
    def __init__(self, target, port_spec="common"):
        self.target = target
        self.ports = self._parse_ports(port_spec)
    
    def _parse_ports(self, spec):
        if spec == "common":
            return self.COMMON_PORTS
        elif "-" in spec:
            start, end = map(int, spec.split("-"))
            return list(range(start, end + 1))
        return self.COMMON_PORTS
    
    def _check_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            return port if result == 0 else None
        except:
            return None
    
    def scan(self):
        open_ports = []
        print(f"  Scanning {len(self.ports)} ports...")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(self._check_port, self.ports)
            for port in results:
                if port:
                    open_ports.append(port)
                    service = self._get_service(port)
                    print(f"  {Fore.GREEN}[+] Port {port} OPEN{Fore.RESET} - {service}")
        
        if not open_ports:
            print(f"  {Fore.YELLOW}[!] No open ports found{Fore.RESET}")
        
        return open_ports
    
    def _get_service(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
            135: "MSRPC", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 1521: "Oracle", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8888: "HTTP-Alt",
            27017: "MongoDB"
        }
        return services.get(port, "Unknown")