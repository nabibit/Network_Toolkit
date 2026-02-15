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

if __name__ == "__main__":
    # Quick self-test
    test = 192
    bin_str = dec_to_bin(test)
    print(f"{test} -> {bin_str} -> {bin_to_dec(bin_str)}")