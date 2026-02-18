#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Basic TCP client to demonstrate the 3-way handshake and HTTP.
# Created: 2026-02-18
# Complexity/Performance: O(1) for single request-response cycle.

"""
Basic TCP client implementation.
Demonstarates raw socket manipulation and TCP 3-way handshake.
"""

import socket

def fetch_http(target:str, port: int) ->str:
    """
    Connect to target via TCP, send an HTTP GET request, and return the response.

    Args:
        target: IP address or hostname (e.g., '127.0.0.1' or 'google.com').
        port: Port number (80 for HTTP, 8000 for local test server).

    Returns:
        The HTTP response as a string.

    Raises:
        ConnectionError: If connection fails or times out.

    Example:
        >>> fetch_http('127.0.0.1', 8000)
        'HTTP/1.0 200 OK...'
    """

    # Use context manager to ensure socket closes (prevents resource leaks)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        # Set timeout to avoid hanging indefinitely if server drops packets
        client.settimeout(5)

        try:
            # Connect - triggers three-way handshake
            client.connect((target, port))

            # Send HTTP GET request
            # 'Connection: close' ensures server terminates stream after sending data
            request = f"GET / HTTP/1.1\r\n Host: {target}\r\n Connection: close\r\n\r\n"
            client.send(request.encode())

            # Receive response (4096 bytes is standrad buffer size)
            respone = client.recv(4096)
            return respone.decode(errors='replace')
 
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            raise ConnectionError(f"Failed to connect to {target}:{port} - {e}")
    
if __name__ == "__main__":
    # Quick self-test (requires local server: python -m http.server 8000)
    target = "127.0.0.1"
    port = 8000
    
    print(f"[*] Connecting to {target}:{port}...")
    try:
        data = fetch_http(target, port)
        print(f"[+] Success. Received {len(data)} bytes.")
        print(f"Response snippet: {data}...")
    except ConnectionError as e:
        print(f"[-] Test failed: {e}")
