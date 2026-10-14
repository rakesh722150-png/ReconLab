#!/usr/bin/env python3
"""
ReconLab - Ethical Bug Bounty Recon Tool
For authorized lab targets only.
"""

import sys
import argparse
from colorama import Fore, init
from modules.port_scanner import PortScanner
from modules.tech_fingerprint import TechFingerprint
from modules.header_analyzer import HeaderAnalyzer
from modules.dir_discovery import DirDiscovery
from modules.report import ReportGenerator

init(autoreset=True, convert=True)


BANNER = f"""
{Fore.CYAN}==========================================================
|                                                        |
|   ReconLab v1.0                                        |
|   --------------------------------------------------   |
|   Ethical Bug Bounty Recon Tool                        |
|                                                        |
|   [!] Lab targets only (127.0.0.1 / private IP)        |
|                                                        |
=========================================================={Fore.RESET}
"""


AUTHORIZED_PREFIXES = [
    "127.", "localhost", "10.", "192.168.",
    "172.16.", "172.17.", "172.18.", "172.19.",
    "172.20.", "172.21.", "172.22.", "172.23.",
    "172.24.", "172.25.", "172.26.", "172.27.",
    "172.28.", "172.29.", "172.30.", "172.31."
]


def is_authorized(target):
    target = target.lower().strip()
    return any(target.startswith(p) for p in AUTHORIZED_PREFIXES)


def detect_web_port(open_ports, port_spec):
    """Detect which port is the web server"""
    # Priority list of web ports
    web_ports = [80, 443, 8080, 8443, 8000, 3000, 5000, 8888, 9000]
    
    # If specific port range given, use that
    if port_spec != "common":
        for p in open_ports:
            if p in web_ports:
                return p
        # If no standard web port, use first open
        if open_ports:
            return open_ports[0]
        return None
    
    # Common scan - find web port
    for wp in web_ports:
        if wp in open_ports:
            return wp
    
    return None


def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(
        description="ReconLab - Ethical Bug Bounty Recon Tool"
    )
    parser.add_argument("target",
                       help="Target host/IP (private only, e.g. 127.0.0.1)")
    parser.add_argument("--ports", "-p", default="common",
                       help="Port range (common | 8080 | 1-1024)")
    parser.add_argument("--report", "-r", default="reports/report.md",
                       help="Report output file")
    parser.add_argument("--skip-dirs", action="store_true",
                       help="Skip directory discovery")
    
    args = parser.parse_args()
    
    if not is_authorized(args.target):
        print(f"{Fore.RED}[!] UNAUTHORIZED TARGET: {args.target}{Fore.RESET}")
        print(f"{Fore.YELLOW}    Only private IPs allowed.{Fore.RESET}")
        print(f"{Fore.YELLOW}    Allowed: 127.x, 10.x, 192.168.x, 172.16-31.x{Fore.RESET}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}[+] Target authorized: {args.target}{Fore.RESET}\n")
    
    results = {
        'target': args.target,
        'ports': [],
        'tech': {},
        'headers': {},
        'directories': []
    }
    
    # Step 1: Port Scan
    print(f"{Fore.CYAN}[1/4] Port Scanning...{Fore.RESET}")
    scanner = PortScanner(args.target, args.ports)
    results['ports'] = scanner.scan()
    
    # Detect web port
    web_port = detect_web_port(results['ports'], args.ports)
    if web_port:
        print(f"\n{Fore.YELLOW}[*] Web service detected on port {web_port}{Fore.RESET}")
    else:
        print(f"\n{Fore.YELLOW}[!] No web service found on open ports{Fore.RESET}")
    
    # Step 2: Tech Fingerprint
    print(f"\n{Fore.CYAN}[2/4] Technology Fingerprinting...{Fore.RESET}")
    fp = TechFingerprint(args.target, web_port)
    results['tech'] = fp.detect()
    
    # Step 3: Header Analysis
    print(f"\n{Fore.CYAN}[3/4] Security Headers Analysis...{Fore.RESET}")
    ha = HeaderAnalyzer(args.target, web_port)
    results['headers'] = ha.analyze()
    
    # Step 4: Directory Discovery
    if not args.skip_dirs:
        print(f"\n{Fore.CYAN}[4/4] Directory Discovery...{Fore.RESET}")
        dd = DirDiscovery(args.target, web_port)
        results['directories'] = dd.discover()
    else:
        print(f"\n{Fore.YELLOW}[4/4] Skipped directory discovery{Fore.RESET}")
    
    # Generate Report
    print(f"\n{Fore.CYAN}[*] Generating report...{Fore.RESET}")
    rg = ReportGenerator(results)
    rg.generate(args.report)
    
    print(f"\n{Fore.GREEN}[+] Recon complete!{Fore.RESET}")
    print(f"{Fore.GREEN}[+] Report: {args.report}{Fore.RESET}")


if __name__ == "__main__":
    main()