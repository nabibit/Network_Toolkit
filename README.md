# Network Toolkit

A collection of Python utilities for network engineers and security students, built as part of my self‑study for the cybersecurity market.

## Current Features

- **Binary conversion** – `dec_to_bin()`, `bin_to_dec()` for IP octets.
- **IP to binary** – `ip_to_bin()` converts dotted decimal to 32‑bit string.
- **Subnet calculations** – `network_address()`, `broadcast_address()`, `host_count()`.
- **Interactive subnet calculator** – command‑line tool that lets you repeatedly calculate network details.


## Installation

```bash
git clone https://github.com/bcyberly/Network_Toolkit.git
cd Network_Toolkit
# (Optional) python -m venv venv
pip install -r requirements.txt
```

## Usage 

### As a Python Library
```bash
from src.ip_utils import dec_to_bin, bin_to_dec

print(dec_to_bin(192))   # '11000000'
print(bin_to_dec('11000000')) # 192
```
### Interactive Subnet Calculator
Run the calculator from the command line:
```bash
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

## Documentation
See docs/LEARNING_LOG.md for the detailed engineering journal, including Packet Tracer labs and Wireshark captures.

## Acknowledgements
Built while studying *Computer Networking: A Top‑Down Approach* (Kurose & Ross)*, *Python Crash Course* (Matthes) and *Practical Packet Analysis (3rd ed.)* (Chris Sanders).