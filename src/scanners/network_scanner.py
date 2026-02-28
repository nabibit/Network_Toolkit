#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Integrated scanner combining ping sweep and threaded port scan.
# Created: 2026-02-27

"""
Integrated Network Scanner Module.
We implement a master script that imports our ping sweeper and port scanner modules.
"""

import argparse
import sys
from datetime import datetime

# We import the core functions from out custom toolkit modules
from .ping_sweeper import ping_sweep
from .port_scanner import scan_target

def parse_ports(port_str: str) -> list:
    """ We convert a comma-separated port string into a list of integers."""
    try:
        return [int(p.strip()) for p in port_str.split(',')]
    except ValueError:
        print("[!] Invalid port list. We require comma-separated integers.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Integrated Network Scanner')
    parser.add_argument('target', help='Target IP or network (CIDR)')
    parser.add_argument('--mode', choices=['ping', 'port', 'both'], default='both',
                        help='Scan mode: ping only, port only, or both (default: both)')
    parser.add_argument('-p', '--ports',
                        default='21,22,23,25,53,80,110,135,139,143,443,993,995,1723,3389,5900,8080',
                        help='Comma-separated ports to scan')
    parser.add_argument('-t', '--threads', type=int, default=50,
                        help='Number of concurrent threads for port scanning')
    parser.add_argument('-o', '--output', help='Output CSV file for port scan results')
    args = parser.parse_args()

    print(f"[*] Starting integrated scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    live_hosts = []

    if args.mode in ('ping', 'both'):
        print(f"\n[*] Commencing ping sweep of {args.target} ...")
        live_hosts = ping_sweep(args.target)
        if not live_hosts:
            print("[!] No live hosts discovered.")
            if args.mode == 'ping':
                return
            
    if args.mode in ('port', 'both'):
        ports_to_scan = parse_ports(args.ports)
        hosts_to_scan = live_hosts if args.mode == 'both' else [args.target]

        for host in hosts_to_scan:
            print(f"\n[*] Scanning {host} for open ports (Threads: {args.threads}) ...")
            open_ports = scan_target(host, ports_to_scan, args.threads, args.output)
            if open_ports:
                print(f"[+] {host} open ports: {open_ports}")
            else:
                print(f"[-] {host}: No open ports found (or all filtered).")

    print(f"\n[*] Integrated scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()