#!/usr/bin/env python3
"""
Interactive Subnet Calculator

Allows user to repeatedly calculate network/broadcats addresses and host counts
for given IP and subnet mask. Uses ip_utils functions.
"""

from ip_utils import network_address, broadcast_address, host_count

def print_welcome():
    print(("\n=== Subnet Calculator ==="))
    print("Enter IP and subnet mask to get network details.")
    print("Type 'quit' at any prompt to exit.\n")

def get_input(prompt):
    """Get non-empty input from user, allowing 'quit' to exit."""
    user_input = input(prompt).strip()
    if user_input.lower() == 'quit':
        return None
    return user_input

def main():
    print_welcome()

    while True:
        # Input handling
        ip = get_input("Enter IP address (e.g., 192.168.1.15):")
        if ip is None:
            break

        mask = get_input("Enter subnet masl (e.g., 255.255.255.0):")
        if mask is None:
            break

        try:
            net = network_address(ip, mask)
            bcast = broadcast_address(ip, mask)
            hosts = host_count(mask)

            print(f"\nResults for {ip}/ {mask}:")
            print(f"  Network address:   {net}")
            print(f"  Broadcast address: {bcast}")
            print(f"  Usable hosts:      {hosts}")

        except ValueError as e:
            # Catch validation errors raised by ip_utils (e.g., invalid IP format)
            print(f"Error: {e}. Please try again.\n")
            continue
        
        again = get_input("Another calculation? (y/n): ")
        if again is None or again.lower() not in('y', 'yes', 'Yes', 'YEs', 'YES'):
            break

    print("Goodbye!")

if __name__ == "__main__":
    main()