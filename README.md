# Network Toolkit

A collection of Python utilities for network engineers and security students, built as part of my self‑study for the cybersecurity market.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [As a Python Library](#as-a-python-library)
  - [Advanced Subnet Calculator](#advanced-subnet-calculator)
  - [TCP Client (Safe Local Test)](#tcp-client-safe-local-test)
- [Testing the Tools](#testing-the-tools)
- [Documentation](#documentation)
- [Week 1 Summary](#week-1-summary)
- [Acknowledgements](#acknowledgements)

## Current Features

- **Binary conversion** – `dec_to_bin()`, `bin_to_dec()` for IP octets.
- **IP to binary** – `ip_to_bin()` converts dotted decimal to 32‑bit string.
- **Subnet calculations** – `network_address()`, `broadcast_address()`, `host_count()`.
- **Advanced subnet calculator** – interactive and CLI tool that accepts dotted or CIDR notation, outputs network, broadcast, first/last host, and total hosts.

- **TCP client** – `fetch_http()` demonstrates raw socket programming and the three‑way handshake.


## Installation

```bash
git clone https://github.com/bcyberly/Network_Toolkit.git
cd Network_Toolkit
# (Optional) python -m venv venv
pip install -r requirements.txt
```

## Usage 

### As a Python Library
Import the functions you need from `src.ip_utils`:

```python
from src.ip_utils import (
    dec_to_bin,
    bin_to_dec,
    ip_to_bin,
    network_address,
    broadcast_address,
    host_count
)

# Binary conversion
print(dec_to_bin(192))          # '11000000'
print(bin_to_dec('11000000'))   # 192

# IP to binary string
print(ip_to_bin('192.168.1.1')) # '11000000101010000000000100000001'

# Subnet calculations
net = network_address('192.168.1.15', '255.255.255.0')
bcast = broadcast_address('192.168.1.15', '255.255.255.0')
hosts = host_count('255.255.255.0')

print(f"Network: {net}")        # Network: 192.168.1.0
print(f"Broadcast: {bcast}")    # Broadcast: 192.168.1.255
print(f"Usable hosts: {hosts}") # Usable hosts: 254
```
### Advanced Subnet Calculator
Run interactively:
```python
python -m src.subnet_calculator
```
Supports both dotted (e.g., `192.0.2.15 255.255.255.0`) and CIDR (e.g., `192.0.2.15/24`) input.

### Example session:
```
=== Advanced Subnet Calculator ===
Enter target network: 192.0.2.15/24

Results for 192.0.2.15 / 255.255.255.0:
    Network address:   192.0.2.0
    Broadcast address: 192.0.2.255
    First usable host: 192.0.2.1
    Last usable host:  192.0.2.254
    Usable hosts:      254
```
For quick one‑off calculations, use CLI mode:
```python
python -m src.subnet_calculator 192.0.2.15/24
```

## TCP Client (Safe Local Test)
To observe a three‑way handshake locally:

1. Start a simple HTTP server: `python -m http.server 8000`

2. In another terminal, run: `python -m src.tcp_client`

3. Capture the loopback interface in Wireshark to see the handshake.

## Testing the Tools
Each module includes a self-test when run directly. For example:

```bash
# Test binary conversion utilities
python src/ip_utils.py
# Expected output: 192 -> 11000000 -> 192

# Start the interactive subnet calculator
python src/subnet_calculator.py

# Test TCP client (requires local server on port 8000)
python src/tcp_client.py
# Expected output: [*] Connecting to 127.0.0.1:8000... 
# [+] Success. Received X bytes.
```

### You can also write your own test scripts using the imported functions – they’re designed to be reusable and reliable.



## Documentation
See docs/LEARNING_LOG.md for the detailed engineering journal, including Packet Tracer labs and Wireshark captures.

The log tracks daily progress, concepts, artifacts, and reflections – from binary conversion to static routing.

## Week 1 Summary

In Week 1, I built the foundation of my Network Toolkit. Starting from binary conversions, I developed a suite of subnet calculation tools, an interactive subnet calculator with CLI support, and a TCP client that demonstrates the three‑way handshake. Along the way, I reinforced theory with Packet Tracer labs (simple LAN, two subnets, static routing) and Wireshark captures (ARP, ICMP, TCP handshake). The learning log documents my daily progress, reflections, and evidence. This week established a solid understanding of networking fundamentals and Python automation – ready for Week 2's deeper dives into scanning and security tools.

## Acknowledgements
Built while studying *Computer Networking: A Top‑Down Approach* (Kurose & Ross), *Python Crash Course* (Matthes) and *Practical Packet Analysis (3rd ed.)* (Chris Sanders).