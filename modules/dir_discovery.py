import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DirDiscovery:
    COMMON_DIRS = [
        'admin', 'login', 'wp-admin', 'phpmyadmin', 'backup',
        'api', 'v1', 'v2', 'test', 'dev', 'staging',
        '.git', '.env', 'robots.txt', 'sitemap.xml',
        'config', 'uploads', 'images', 'css', 'js',
        'dashboard', 'user', 'account', 'settings'
    ]
    
    def __init__(self, target, port=None):
        self.target = target
        self.port = port
    
    def _build_url(self, path):
        if self.port and self.port not in [80, 443]:
            return f"http://{self.target}:{self.port}/{path}"
        return f"http://{self.target}/{path}"
    
    def discover(self):
        found = []
        
        for path in self.COMMON_DIRS:
            try:
                url = self._build_url(path)
                r = requests.get(url, timeout=3, verify=False, 
                                allow_redirects=False)
                
                if r.status_code in [200, 301, 302, 401, 403]:
                    found.append({'path': f"/{path}", 
                                 'status': r.status_code})
                    color = (Fore.GREEN if r.status_code == 200 
                            else Fore.YELLOW)
                    print(f"  {color}[+] /{path} - {r.status_code}{Fore.RESET}")
            except:
                continue
        
        if not found:
            print(f"  {Fore.YELLOW}[!] No common directories found{Fore.RESET}")
        
        return found