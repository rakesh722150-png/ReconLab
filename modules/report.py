from datetime import datetime


class ReportGenerator:
    def __init__(self, results):
        self.results = results
    
    def generate(self, filename):
        target = self.results['target']
        ports = self.results['ports']
        tech = self.results['tech']
        headers = self.results['headers']
        dirs = self.results['directories']
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# ReconLab Report\n\n")
            f.write(f"**Target:** `{target}`\n\n")
            f.write(f"**Date:** {datetime.now()}\n\n")
            f.write("---\n\n")
            
            f.write(f"## Open Ports ({len(ports)})\n\n")
            if ports:
                for p in ports:
                    f.write(f"- Port {p}\n")
            else:
                f.write("No open ports\n")
            f.write("\n")
            
            f.write(f"## Technology\n\n")
            for k, v in tech.items():
                f.write(f"- **{k}:** {v}\n")
            f.write("\n")
            
            f.write(f"## Security Headers\n\n")
            for k, v in headers.items():
                f.write(f"- **{k}:** {v}\n")
            f.write("\n")
            
            f.write(f"## Directories ({len(dirs)})\n\n")
            if dirs:
                for d in dirs:
                    f.write(f"- `{d['path']}` - {d['status']}\n")
            else:
                f.write("No common directories found\n")
        
        print(f"  [+] Report saved: {filename}")