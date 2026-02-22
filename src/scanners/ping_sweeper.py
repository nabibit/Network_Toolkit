#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Ping sweep tool to discover live hosts on a network.
# Created: 2026-02-22
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
    # Default to a safe /24 network - change to your own LAN if desired
    network_str = "192.168.1.0/24"

    try:
        network = ipaddress.ip_network(network_str, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network: {e}")
        sys.exit(1)

    print(f"[*] Scanning {network_str} from a {platform.system()} machine...\n")

    hosts = list(network.hosts()) # Convert to a list so we can count them
    total_hosts = len(hosts)

    results = {}
    for i, ip in enumerate(hosts, 1):
        # Write progress to the same line using \r (carriage return)
        sys.stdout.write(f"\r[*] Progress: {i}/ {total_hosts} ({(i/total_hosts)*100:.1f}%)")
        sys.stdout.flush() # Force the terminal to update instantly

        status = ping_host(ip)
        results[str(ip)] = status

        if status:
            # Overwrite the progress line with the hit, addig space to clear old text
            print(f"[+] {ip} is UP{' '*30}")

    up_count = sum(1 for status in results.values() if status)
    print(f"\n[*] Scan complete. {up_count} hosts up.")

if __name__ == "__main__":
    main()