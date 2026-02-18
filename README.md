# Network Toolkit

A collection of Python utilities for network engineers and security students, built as part of my self‑study for the cybersecurity market.

## Current Features

- **Binary conversion** – `dec_to_bin()`, `bin_to_dec()` for IP octets.
- **IP to binary** – `ip_to_bin()` converts dotted decimal to 32‑bit string.
- **Subnet calculations** – `network_address()`, `broadcast_address()`, `host_count()`.
- **Interactive subnet calculator** – command‑line tool that lets you repeatedly calculate network details.
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

```bash
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
### Interactive Subnet Calculator
Run the calculator from the command line:
```python
python -m src.subnet_calculator
```
You'll be prompted to enter an IP and subnet mask. Type quit at any prompt to exit.

### Example session:
```python
=== Subnet Calculator ===
Enter IP address (e.g., 192.168.1.15): 192.168.1.15
Enter subnet mask (e.g., 255.255.255.0): 255.255.255.0

Results for 192.168.1.15 / 255.255.255.0:
  Network address:   192.168.1.0
  Broadcast address: 192.168.1.255
  Usable hosts:      254

Another calculation? (y/n): n
Goodbye!
```

## TCP Client (Safe Local Test)
To observe a three‑way handshake locally:

1. Start a simple HTTP server: `python -m http.server 8000`

2. In another terminal, run: `python -m src.tcp_client`

3. Capture the loopback interface in Wireshark to see the handshake.

## Testing the Tools
Each module includes a self-test when run directly. For example:

```bash
python src/ip_utils.py        # runs quick binary conversion test
python src/subnet_calculator.py  # starts interactive tool
python src/tcp_client.py      # connects to local server (if running)
```
### You can also write your own test scripts using the imported functions – they’re designed to be reusable and reliable.



## Documentation
See docs/LEARNING_LOG.md for the detailed engineering journal, including Packet Tracer labs and Wireshark captures.

## Acknowledgements
Built while studying *Computer Networking: A Top‑Down Approach* (Kurose & Ross)*, *Python Crash Course* (Matthes) and *Practical Packet Analysis (3rd ed.)* (Chris Sanders).