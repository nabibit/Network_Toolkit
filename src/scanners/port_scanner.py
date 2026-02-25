#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: TCP port scanner to discover open ports on a target.
# Created: 2026-02-25
# Complexity: O(N) where n is the number of ports scanned.

"""
TCP Port Scanner Module.
We implement a simple TCP connect scanner to identify open ports on a target host.
"""

import socket
import sys
import argparse
from datetime import datetime
from typing import List

def scan_port(ip: str, port: int) -> bool:
    """
    We attempt to connect to a specific TCP port on the target IP.
    
    Args:
        ip: Target IP address.
        port: Port number to scan.
        
    Returns:
        bool: True if the port is open, False otherwise.
    """
    try:
        # We utilize a context manager to ensure the socket closes cleanly after the operation.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # We set a 1-second timeout to prevent the script from hanging on filtered or dropped packets.
            sock.settimeout(1)

            # We use connect_ex(), which returns a C-style error indicator (0 for success)
            # instead of raising an exception for closed ports.
            result = sock.connect_ex((ip,port))
            return result == 0
        
    except socket.error:
        # We catch any low-level socket errors and assume the port is inaccessible.
        return False
    
def scan_target(ip: str, ports: List[int]) -> List[int]:
    """
    We iterate through a list of ports to scan the target IP.
    """
    open_ports = []
    for port in ports:
        if scan_port(ip, port):
            open_ports.append(port)
            print(f"[+] Port {port} is OPEN")
    return open_ports
    
# ---------------------------------------------------
# Local Test Area & CLI
if __name__ == "__main__":
    # We initialize the argument parser to handle CLI inputs and generate the help menu.
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("target", help = "Target IP address")
    parser.add_argument("-p", "--ports",
                        default = "21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080",
                        help= "Comma-separated ports to scan (default: common ports)")
    args = parser.parse_args()

    try:
        # We convert the comme-separated string provided by the user into a list of integers.
        ports_to_scan = [int(p.strip()) for p in args.ports.split(",")]
    except ValueError:
        print("[!] Invalid port list. We require comma-separated integers.")
        sys.exit(1)

    print(f"[*] Scanning {args.target} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Ports to scan: {ports_to_scan}\n")

    # We execute the scan against the target using the parsed arguments.
    found_ports = scan_target(args.target, ports_to_scan)

    print(f"\n[*] Scan completed. Open ports: {found_ports}")