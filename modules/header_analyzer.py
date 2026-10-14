import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HeaderAnalyzer:
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'HSTS missing - HTTPS downgrade possible',
        'X-Frame-Options': 'Clickjacking risk',
        'X-Content-Type-Options': 'MIME sniffing risk',
        'Content-Security-Policy': 'XSS protection weak',
        'X-XSS-Protection': 'XSS filter missing',
        'Referrer-Policy': 'Referrer leakage',
        'Permissions-Policy': 'Feature policy missing'
    }
    
    def __init__(self, target, port=None):
        self.target = target
        self.port = port
    
    def _build_url(self):
        if self.port and self.port not in [80, 443]:
            return f"http://{self.target}:{self.port}"
        return f"http://{self.target}"
    
    def analyze(self):
        results = {}
        
        try:
            url = self._build_url()
            r = requests.get(url, timeout=5, verify=False)
            
            for header, warning in self.SECURITY_HEADERS.items():
                if header in r.headers:
                    results[header] = f"Present: {r.headers[header]}"
                    print(f"  {Fore.GREEN}[+] {header}{Fore.RESET}")
                else:
                    results[header] = f"MISSING - {warning}"
                    print(f"  {Fore.RED}[-] {header} - {warning}{Fore.RESET}")
        
        except Exception as e:
            print(f"  {Fore.YELLOW}[!] No web service on port {self.port or 80}{Fore.RESET}")
        
        return results