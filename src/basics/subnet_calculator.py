#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Interactive and CLI subnet calculator with VLSM (CIDR) support.
# Created: 2026-02-19
# Complexity: O(1) - Constant time address calculations per request.

"""
Advanced Subnet Calculator Module.

Acts as the user interface (CLI) for the ip_utils library.
Provides both an interactive REPL and a command-line interface (CLI) for
calculating subnet boundaries, broadcast addresses, and host ranges.
Support both dotted-decimal and CIDR notation.
"""
import argparse
import sys
from src.utils.ip_utils import network_address, broadcast_address, host_count, bin_to_dec

def parse_cidr(cidr: str) -> tuple[str, str]:
    """
    Convert CIDR notation (e.g., '192.168.1.0/24') to an IP and dotted-decimal mask.
    
    Args:
        cidr: String in CIDR format.
    
    Returns:
        Tuple containing (ip_address, subnet_mask).        
    """
    try:
        ip, prefix_str = cidr.split('/')
        prefix = int(prefix_str)

        if not 0 <= prefix <= 32:
            raise ValueError(f"CIDR prefix must be between 0 and 32, got {prefix}")
        
        # Generate the 32-bit binary mask string
        mask_bin = '1' * prefix + '0' * (32 - prefix)

        # Chunk into 8 bits and convert using our custom bin_to_dec function
        octets = [str(bin_to_dec(mask_bin[i:i+8])) for i in range (0, 32, 8)]
        mask = '.'.join(octets)

        return ip, mask
    
    except ValueError:
        raise ValueError(f"Invalid CIDR notation: {cidr}")
    
def get_host_range(network: str, broadcast: str, hosts: int) -> tuple[str, str]:
    """
    Calculate the first and last usable host addresses in subnet.

    Args: 
        network: Dotted-decimal network address.
        broadcast: Dotted-decimal broadcast address.
        hosts: Number of usable hosts.

    Returns:
        Tuple containing (first_host, last_host) or ('N/A', 'N/A') for /31 & /32.
    """
    # /31 (point-to-point) and /32 (host route) have no standard "usable host" range
    if hosts <= 0:
        return "N/A", "N/A"

    net_octets = list(map(int, network.split('.')))
    bcast_octets = list(map(int, broadcast.split('.')))

    # Because IPv4 host bits occupy the rightmost positions, we can safely
    # find the boundaries by adjusting the 4th octet for /30 and larger subnets
    first = net_octets.copy()
    first[3] += 1 
    
    last = bcast_octets.copy()
    last[3] -= 1

    return '.'.join(map(str, first)), '.'.join(map(str, last))

def calculate_subnet(ip: str, mask: str) -> dict:
    """
    Perform all subnet calculations and aggregate the results.
    Returns a dicitionary to cleanly separate logic from presentation.
    """
    net = network_address(ip, mask)
    bcast = broadcast_address(ip, mask)
    hosts = host_count(mask)
    first, last = get_host_range(net, bcast, hosts)

    return {
        'ip': ip,
        'mask': mask,
        'network': net,
        'broadcast': bcast,
        'first': first,
        'last': last,
        'hosts': hosts
    }

def print_results(res: dict):
    """ Standardized output formatter for both CLI and Interactive modes."""
    print(f"\nResults for {res['ip']} / {res['mask']}:")
    print(f"    Network address:   {res['network']}")
    print(f"    Broadcast address: {res['broadcast']}")
    print(f"    First usable host: {res['first']}")
    print(f"    Last usable host:  {res['last']}")
    print(f"    Usable hosts:      {res['hosts']}\n")

def interactive_mode():
    """ Interactive loop for reperated calculations."""
    print("\n=== Advanced Subnet Calculator ===")
    print("Supports CIDR (192.168.1.1/24) or Space-Separated (192.168.1.1 255.255.255.0)")
    print("Type 'quit' at any prompt to exit.\n")

    while True:
        inp = input("Enter target network: ").strip()
        if not inp or inp.lower() == 'quit':
            break

        try:
            if '/' in inp:
                ip, mask = parse_cidr(inp)
            else:
                # Handle space-separated inputs robustly
                parts = inp.split()
                if len(parts) != 2:
                    print("[!] Invalid format. Use 'ip/mask' or 'ip mask.\n")
                    continue
                ip, mask = parts[0], parts[1]

            results = calculate_subnet(ip, mask)
            print_results(results)
        
        except ValueError as e:
            print(f"[!] Error: {e}\n")

def cli_mode():
    """Command-line execution mode using argparse."""
    parser = argparse.ArgumentParser(description="Calculate subnet boundaries and host ranges.")

    # We enforce CIDR in CLI mode to keep the argument structure clean
    # and avoid issues in shell string parsing.
    parser.add_argument(
        "cidr",
        help="Target network in CIDR notation (e.g., 10.0.0.0/24)"
    )

    args = parser.parse_args()

    try: 
        if '/' not in args.cidr:
            print("[!] Error: CLI mode requires CIDR notation (e.g., 192.168.1.0/24)")
            sys.exit(1)

        ip, mask = parse_cidr(args.cidr)
        results = calculate_subnet(ip, mask)
        print_results(results)

    except ValueError as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Route execution based on whether command-line arguments were provided.
    # sys.argv[0] is the script name; anything beyond that is an argument.
    if len(sys.argv) > 1:
        cli_mode()
    else: 
        interactive_mode()