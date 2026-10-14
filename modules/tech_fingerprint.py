import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TechFingerprint:
    def __init__(self, target, port=None):
        self.target = target
        self.port = port
    
    def _build_url(self, scheme):
        if self.port and self.port not in [80, 443]:
            return f"{scheme}://{self.target}:{self.port}"
        return f"{scheme}://{self.target}"
    
    def detect(self):
        results = {}
        
        for scheme in ['http', 'https']:
            try:
                url = self._build_url(scheme)
                r = requests.get(url, timeout=5, verify=False, 
                                allow_redirects=True)
                
                server = r.headers.get('Server', 'Unknown')
                results['server'] = server
                print(f"  [+] Server: {server}")
                
                powered = r.headers.get('X-Powered-By', 'Not set')
                results['powered_by'] = powered
                print(f"  [+] X-Powered-By: {powered}")
                
                html = r.text.lower()
                techs = []
                if 'wordpress' in html: techs.append('WordPress')
                if 'joomla' in html: techs.append('Joomla')
                if 'drupal' in html: techs.append('Drupal')
                if 'django' in html: techs.append('Django')
                if 'laravel' in html: techs.append('Laravel')
                if 'react' in html: techs.append('React')
                if 'angular' in html: techs.append('Angular')
                
                if techs:
                    results['cms'] = ', '.join(techs)
                    print(f"  [+] Framework: {', '.join(techs)}")
                
                results['status_code'] = r.status_code
                break
            except Exception as e:
                continue
        
        if not results:
            print(f"  [!] No web service detected")
        
        return results