#!/usr/bin/env python3
"""
Simple subnet calculator - demonstartes ip_utils functions.
For now, uses hardcoded IP and mask; will be enhaced later.
"""

from ip_utils import network_address, broadcast_address, host_count

def main():
    # Hardcoded example - later we'll add argparse
    ip = '192.168.1.100'
    mask = '255.255.255.0'

    print(f"Ip: {ip}")
    print(f"Mask: {mask}")
    print(f"Network address: {network_address(ip,mask)}")
    print(f"Broadcast address: {broadcast_address(ip, mask)}")
    print(f"Usable hosts: {host_count(mask)}")

if __name__ == "__main__":
    main()