#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Ping sweep tool to discover live hosts on a network.
# Created: 2026-02-22
# Updated: 2026-02-24 (added argparse, down_count summary)
# Complexity: O(n) where n is number of hosts scanned.

"""
Ping sweeper that uses system ping to check host availability.
Demonstrates network scanning fundamentals before introducing Scapy.
Includes cross-platform support for Windows and Unix-like systems.
"""

import subprocess
import ipaddress
import platform
import sys
import argparse # Added to handle command-line arguments (e.g., --network)

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
    
def main():
    # We initialize the ArgumentParser object to handle command-line inputs and build a help menu (-h)
    parser = argparse.ArgumentParser(description="Ping sweep a network to find live hosts.")
    parser.add_argument('--network', '-n',
                        default='192.168.1.0/24',
                        help='Network range in CIDR notation (e.g., 192.168.1.0/24)')
    args = parser.parse_args()

    try:
        # We parse the input string into a network object, using the CLI argument
        network = ipaddress.ip_network(args.network, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network: {e}")
        sys.exit(1)

    print(f"[*] Scanning {args.network} from a {platform.system()} machine...\n")

    # We convert the generator to a list to ascertain the total number of target hosts
    hosts = list(network.hosts())
    total_hosts = len(hosts)

    results = {}
    for i, ip in enumerate(hosts, 1):
        #  We utilize a carriage return (\r) to overwrite the current line, preventing terminal spam
        sys.stdout.write(f"\r[*] Progress: {i}/ {total_hosts} ({(i/total_hosts)*100:.1f}%)")
        sys.stdout.flush() # We force the terminal to update instantly

        status = ping_host(ip)
        results[str(ip)] = status

        if status:
            # We overwrite the progress line with the hit, adding spaces to clear old text
            print(f"\n[+] {ip} is UP{' '*30}")

    # We aggragate the results to calculate the total number of online and offline hosts
    up_count = sum(1 for status in results.values() if status)
    down_count = total_hosts - up_count
    
    print(f"\n[*] Scan complete. We discovered {up_count} hosts up, and {down_count} hosts down.")

if __name__ == "__main__":
    main()