#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Ping sweep tool to discover live hosts on a network.
# Created: 2026-02-22
# Updated: 2026-02-27 (refactored for modularity)
# Complexity: O(n) where n is number of hosts scanned.

"""
Ping Sweeper Module.
We use system ping to check host availability across a subnet.
We refactored this module to expose ping_sweep() for integration into larger frameworks.
Includes cross-platform support for Windows and Unix-like systems.
"""

import subprocess
import ipaddress
import platform
import sys
import argparse 

def ping_host(ip: str | ipaddress.IPv4Address) -> bool:
    """
    Ping a single IP address and return True if host responds.

    Args:
        ip: ipaddress.IPv4Address object or string.

    Returns:
        bool: True if ping successful, False otherwise.
    """

    current_os = platform.system().lower()

    # Windows uses -n for count and -w for timeout (in milliseconds)
    # Unix uses -c for count and -W for timeout (in seconds)
    if current_os == "windows":
        cmd = ['ping', '-n', '1', '-w', '1000', str(ip)]
    else:
        cmd = ['ping', '-c', '1', '-W', '1', str(ip)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False
    
def ping_sweep(network_str: str) -> list:
    """
    We perform a ping weep on a network and return a list of responsive IPs.
    """
    try:
        network = ipaddress.ip_network(network_str, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network: {e}")
        sys.exit(1)

    hosts = list(network.hosts())
    total_hosts = len(hosts)
    live_hosts = []
    
    for i, ip in enumerate(hosts, 1):
        #  We utilize a carriage return (\r) to overwrite the current line, preventing terminal spam
        sys.stdout.write(f"\r[*] Progress: {i}/ {total_hosts} ({(i/total_hosts)*100:.1f}%)")
        sys.stdout.flush() # We force the terminal to update instantly

        if ping_host(ip):
            live_hosts.append(str(ip))
            # We overwrite the progrss line with the hit, adding spaces to clear old text
            sys.stdout.write(f"\r[+] {ip} is UP{' '*30}\n")

    print(f"\n[*] Ping sweep complete. We found {len(live_hosts)} live hosts.")
    return live_hosts

def main():
    # We intialize the argument parser for standalone CLI execution.
    parser = argparse.ArgumentParser(description="Ping sweep a network to find live hosts.")
    parser.add_argument('--network', '-n',
                        default='192.168.1.0/24',
                        help='Network range in CIDR notation (e.g., 192.168.1.0/24)')
    args = parser.parse_args()

    print(f"[*] Scanning {args.network} from a {platform.system()} machine...\n")

    # We call our newly extracted function.
    ping_sweep(args.network)

if __name__ == "__main__":
    main()