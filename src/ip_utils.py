# Project: Network Toolkit
# Purpose: Core networking math functions (binary/ hex conversions)
#          used by other tools in the toolkit.
# Created: 2026-02-15
# Complexity/Performance: O(1) for fixed 8-bit input.

"""
Utility functions for network address calculations.
Provides decimal-binary conversions with validation,
forming the foundation for subnet calculations.
"""

def dec_to_bin(octet: int) -> str:
    """
    Convert decimal octet (0-255) to 8-bit binary string.

    Args:
        octet: Integer between 0 and 255.

    Returns:
        8-character binary string, padded with leading zeros.

    Raises:
        ValueError: If octet out of range.

    Example:
        >>> dec_to_bin(192)
        '11000000'
    """

    if not 0 <= octet <= 255:
        raise ValueError(f"Octet must be 0-255, got {octet}")
    
    # bin() gives '0b' prefix; slice off prefix and pad to 8 bits
    # Padding is crtical because IP maths expects full octets
    return bin(octet)[2:].zfill(8)

def bin_to_dec(binary: str) -> int:
    
    """
    Convert 8=bit binary string to decimal integer.

    Args:
        binary: String of 8 characters, each '0' or '1'.

    Returns:
        Integer value.

    Raises:
        ValueError: If input is not valid 8-bit binary.

    Example:
        >>> bin_to_dec('11000000')
        192
    """

    if len(binary) != 8 or not all(c in '01' for c in binary):
        raise ValueError("Binary must be 8 bits of 0/1")
    
    # int(binary,2) is the stard way to parse binary strings
    return int(binary, 2)

def ip_to_bin(ip: str) ->str:
    """
    Convert dotted decimal IP to 32-bit binary string.
    
    Args:
        ip: IPv4 address as string (e.g., '192.168.1.1')
    
    Returns:
        32-character binary string
    
    Raises:
        ValueError: If IP format is invalid
    """

    octets = ip.split('.')
    if len(octets) != 4:
        raise ValueError(f"Invalid IP format: {ip}")
    
    binary_parts = []
    for octet in octets:
        try:
            val = int(octet)
            # Reuses dec_to_bin to get 8-bit binary
            binary_parts.append(dec_to_bin(val))
        except ValueError:
            raise ValueError(f"Invalid octet in IP: {octet}")
    return ''.join(binary_parts)
    
def network_address(ip: str, mask: str) -> str:
    """
    Calculate network address given IP and subnet mask

    Args:
        ip: IPv4 address string
        mask: Subnet mask string (dotted decimal, e.g., '255.255.255.0')

    Returns:
        Network address as dotted decimal string

    Example:
        >>> network_address('192.168.1.100', '255.255.255.0')
        '192.168.1.0'
 
    """
    ip_bin = ip_to_bin(ip)
    mask_bin = ip_to_bin(mask) # mask is also an IP-like string

    # Bitwise AND on each bit (as string) - could also convert to int but this is explicit
    network_bin = ''.join(str(int(ip_bin[i] == '1' and mask_bin[i] == '1')) for i in range(32))

    # Convert back to dotted decimal
    octets = [str(int(network_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    return '.'.join(octets)

def broadcast_address(ip: str, mask: str) -> str:
    """
    Calculate broadcast address given IP and subnet mask
    
    Args:
        ip: IPv4 address string
        mask: Subnet mask string

    Returns:
        Broadcast address as dotted decimal string
    """
    ip_bin = ip_to_bin(ip)
    mask_bin = ip_to_bin(mask)

    # Invert mask for host bits: 0 becomes 1, 1 becomes 0
    wildcard_bin = ''.join('1' if bit == '0' else '0' for bit in mask_bin)

    # OR ip with wildcard to get broadcast 
    broadcast_bin = ''.join(str(int(ip_bin[i] == '1' or wildcard_bin[i] == '1')) for i in range(32))

    octets = [str(int(broadcast_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    return '.'.join(octets)

def host_count(mask: str) -> int:
    """
    Calculate number of usable hosts for a given subnet mask

    Args:
        mask: Subnet mask string (dotted decimal)

    Returns: 
        Number of usable hosts (2^(32-number of prefix bits) - 2)
    """
    mask_bin = ip_to_bin(mask)
    prefix_len = mask_bin.count('1')
    return (1 << (32 - prefix_len)) - 2
    
if  __name__ == "__main__":
    #Quick self-test
    test = 192
    bin_str = dec_to_bin(test)
    print(f"{test} -> {bin_str} -> {bin_to_dec(bin_str)}")