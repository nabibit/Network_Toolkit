#!/usr/bin/env python3
# Project: Network Toolkit
# Purpose: Multithreaded TCP port scanner with CSV export capabilities.
# Created: 2026-02-25
# Complexity: O(N/T) where N is ports and T is threads, Space O(N) for the queue.

"""
Multithreaded TCP Port Scanner Module.
We implement a threaded worker queue to scan target ports concurrently,
drastically reducing scan times, and provide a CSV export for reporting.
"""

import socket
import sys
import argparse
import csv
import threading
from queue import Queue 
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
    
def scan_worker(ip: str, port_queue: Queue, open_ports: List[int]) -> None:
    """
    We process ports from the queue concurrently.
    Each thread pulls a port from the queue, scans it, and logs it if open.
    """
    while not port_queue.empty():
        # We retrieve the next port number from the thread-safe queue.
        port = port_queue.get()

        if scan_port(ip, port):
            open_ports.append(port)
            print(f"[+] Port {port} is OPEN")

        # We signal to the queue that the processing for this specific task is complete.
        port_queue.task_done()
    
# ---------------------------------------------------
# Local Test Area & CLI
if __name__ == "__main__":
    # We initialize the argument parser to handle CLI inputs and generate the help menu.
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("target", help = "Target IP address")
    parser.add_argument("-p", "--ports",
                        default = "21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080",
                        help= "Comma-separated ports to scan (default: common ports)")
    parser.add_argument("-o", "--output",
                        help="Output file to save results (e.g., results.csv)")
    parser.add_argument("-t", "--threads", type=int, default=50,
                        help="Number of concurrent threads (default: 50)")
    args = parser.parse_args()

    try:
        # We convert the comme-separated string provided by the user into a list of integers.
        ports_to_scan = [int(p.strip()) for p in args.ports.split(",")]
    except ValueError:
        print("[!] Invalid port list. We require comma-separated integers.")
        sys.exit(1)

    print(f"[*] Scanning {args.target} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Ports to scan: {ports_to_scan}\n")

    # We initialize the thread-safe queue and populate it with our target ports.
    port_queue = Queue()
    for port in ports_to_scan:
        port_queue.put(port)

    open_ports = []
    threads = []

    # We spawn the specified number of worker threads
    for _ in range(args.threads):
        t = threading.Thread(target=scan_worker, args=(args.target, port_queue, open_ports))
        t.daemon = True
        t.start()
        threads.append(t)

    # We block the main thread until the queue is completely empty
    port_queue.join()

    # We sort the final list so the output is sequentially redable
    open_ports.sort()
    print(f"\n[*] Scan completed. Open ports: {open_ports}")

    # We handle the optional CSV export if requested by the user
    if args.output:
        try:
            with open(args.output, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Target", "Port", "Status"])
                for p in open_ports:
                    writer.writerow([args.target, p, "OPEN"])
            print(f"[*] results saved to {args.output}")

        except Exception as e:
            print(f"[!] We encountered an error writing to CSV: {e}")