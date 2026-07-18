# Network Toolkit

![Networking](https://img.shields.io/badge/Networking-IPv4_/_IPv6-blue)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![Wireshark](https://img.shields.io/badge/Wireshark-Packet_Analysis-brightgreen)
![Nmap](https://img.shields.io/badge/Nmap-Network_Scanning-red)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-orange)

A collection of Python utilities for network engineers and security students, built as part of my self‑study for the cybersecurity market.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [As a Python Library](#as-a-python-library)
  - [Advanced Subnet Calculator](#advanced-subnet-calculator)
  - [TCP Client (Safe Local Test)](#tcp-client-safe-local-test)
  - [Ping Sweeper](#ping-sweeper)
  - [TCP Port Scanner](#tcp-port-scanner)
  - [Integrated Network Scanner](#integrated-network-scanner)
- [Testing the Tools](#testing-the-tools)
- [Documentation](#documentation)
- [Week 1 Summary](#week-1-summary)
- [Week 2 Summary](#week-2-summary)
- [Acknowledgements](#acknowledgements)

## Current Features

- **Binary conversion** – `dec_to_bin()`, `bin_to_dec()` for IP octets.
- **IP to binary** – `ip_to_bin()` converts dotted decimal to 32‑bit string.
- **Subnet calculations** – `network_address()`, `broadcast_address()`, `host_count()`.
- **Advanced subnet calculator** – interactive and CLI tool that accepts dotted or CIDR notation, outputs network, broadcast, first/last host, and total hosts.
- **TCP client** – `fetch_http()` demonstrates raw socket programming and the three‑way handshake.
- **Ping sweeper** – cross‑platform tool (`ping_sweeper.py`) to discover live hosts on a network. Supports CIDR input via `--network`, includes live progress indicator, and stores results in a dictionary.
- **TCP port scanner** – multi‑threaded scanner with custom port lists, adjustable thread count, and CSV export.
- **Integrated network scanner** – combines ping sweep and threaded port scan (`network_scanner.py`) with `--mode` selection (ping/port/both). Automatically discovers live hosts and scans them for open ports.

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
from src.utils.ip_utils import (
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

**Interactive mode:** start the tool, then enter networks at the prompt:

```bash
python -m src.basics.subnet_calculator
```
Supports dotted notation (e.g., 192.0.2.15 255.255.255.0) or CIDR notation (e.g., 192.0.2.15/24) input.

CLI mode: 

calculate in one line:
```bash
python -m src.basics.subnet_calculator 192.0.2.15/24
```
Example interactive session:
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

### TCP Client (Safe Local Test)
To observe a three‑way handshake locally:

1. Start a simple HTTP server: `python -m http.server 8000`

2. In another terminal, run: `python -m src.basics.tcp_client`

3. Capture the loopback interface in Wireshark to see the handshake.

### Ping Sweeper
Discover live hosts on a network using ICMP ping. Automatically detects your operating system and uses the correct ping flags.

By default, the script scans `192.168.1.0/24`. Use the `--network` argument to scan a different range:
```bash
python -m src.scanners.ping_sweeper --network 10.0.0.0/24
```

### TCP Port Scanner
Scan a target for open TCP ports using a multi‑threaded connect scanner.

```bash
# Scan with default common ports (50 threads)
python -m src.scanners.port_scanner 192.168.1.1

# Scan with custom ports and 100 threads
python -m src.scanners.port_scanner scanme.nmap.org -p 22,80,443,8080 -t 100

# Scan and save results to CSV
python -m src.scanners.port_scanner 10.0.0.1 -o results.csv
```

### Integrated Network Scanner
Unifies ping sweep and port scan for automated network reconnaissance.

```bash
# Ping sweep only
python -m src.scanners.network_scanner 192.168.1.0/28 --mode ping

# Port scan a single IP (with threading and CSV output)
python -m src.scanners.network_scanner scanme.nmap.org --mode port -p 22,80,443 -t 50 -o results.csv

# Both: ping sweep then port scan each live host, save JSON
python -m src.scanners.network_scanner 192.168.1.0/24 --mode both -p 22,80,443 -t 50 -j scan.json
```

**Options:**
- `target` – IP address or network in CIDR notation (required).
- `--mode` – `ping`, `port`, or `both` (default: `both`).
- `-p, --ports` – Comma-separated list of ports (default: common ports list).
- `-t, --threads` – Number of concurrent threads (default: 50).
- `-o, --output` – Output CSV file name (optional, port mode only).
- `-j, --json FILE` – Output results in JSON format to specified file.

---

### Optional Quick Test
```bash
python -m src.scanners.network_scanner 127.0.0.1/32 --mode ping
```
Expected output shows localhost is up.

## Testing the Tools

Each module includes a self-test or can be run directly to verify functionality. Run these commands from the project root (`Network_Toolkit/`).

---

### Binary Conversion Utilities
```bash
python -m src.ip_utils
```

**Expected output:**
```
192 -> 11000000 -> 192
```

---

### Interactive Subnet Calculator
```bash
python -m src.basics.subnet_calculator
```

Then follow the prompts. Example session:

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

---

### TCP Client (Requires Local HTTP Server)

First, start a local server:

```bash
python -m http.server 8000
```

Then, in another terminal, run the client:

```bash
python -m src.basics.tcp_client
```

**Expected output (snippet):**

```
[*] Connecting to 127.0.0.1:8000...
[+] Success. Received X bytes.
Response snippet: <!DOCTYPE HTML>...
```

---

### Ping Sweeper
```bash
python -m src.scanners.ping_sweeper --network 192.168.1.0/28
```

Scans a small network (adjust to your own range).

Example output:

```
[*] Scanning 192.168.1.0/28 from a Windows machine...

[*] Progress: 14/14 (100.0%)
[+] 192.168.1.1 is UP

[*] Scan complete. 1 hosts up, 13 hosts down.
```

---

### TCP Port Scanner
```bash
python -m src.scanners.port_scanner scanme.nmap.org -p 22,80,443
```

**Expected output:**

```
[*] Scanning scanme.nmap.org at 2026-02-25 15:30:00
[*] Ports to scan: [22, 80, 443]
[*] Using 50 threads

[+] Port 22 is OPEN
[+] Port 80 is OPEN

[*] Scan completed. Open ports: [22, 80]
```

For CSV output, add:

```bash
-o results.csv
```

---

### Integrated Network Scanner (Quick Test)
```bash
python -m src.scanners.network_scanner 127.0.0.1/32 --mode ping
```

**Expected output:**

```
[*] Starting integrated scan at 2026-02-27 15:30:00
[*] Ping sweeping 127.0.0.1/32 ...
[*] Progress: 1/1 (100.0%)
[+] 127.0.0.1 is UP
[*] Ping sweep complete. Found 1 live hosts.
[*] Scan completed at 2026-02-27 15:30:02
```

You can also test full functionality:

```bash
python -m src.scanners.network_scanner 127.0.0.1/32 --mode both -p 22,80,443 -t 50 -j test.json
```

### You can also write your own test scripts using the imported functions – they’re designed to be reusable and reliable.



## Documentation
See docs/LEARNING_LOG.md for the detailed engineering journal, including Packet Tracer labs and Wireshark captures.

The log tracks daily progress, concepts, artifacts, and reflections – from binary conversion to static routing.

---

## Week 1 Summary

In Week 1, I built the foundation of my Network Toolkit. Starting from binary conversions, I developed a suite of subnet calculation tools, an interactive subnet calculator with CLI support, and a TCP client that demonstrates the three‑way handshake. Along the way, I reinforced theory with Packet Tracer labs (simple LAN, two subnets, static routing) and Wireshark captures (ARP, ICMP, TCP handshake). The learning log documents my daily progress, reflections, and evidence. This week established a solid understanding of networking fundamentals and Python automation – ready for Week 2's deeper dives into scanning and security tools.

---

## Week 2 Summary

In Week 2, I moved from foundational theory to active network exploration and tool development. I built a cross‑platform ping sweeper with CIDR input and progress indicators, then evolved it into a multithreaded TCP port scanner with CSV export. The week's flagship achievement is the integrated network scanner (`network_scanner.py`), which combines ping sweep and port scan into one tool with `--mode` selection and JSON output. I also deepened my understanding of Nmap through hands‑on exploration of timing templates, OS detection, and the Nmap Scripting Engine (NSE). Throughout the week, I reinforced concepts with Packet Tracer labs (VLANs, static routing). The repository is now professionally structured with `utils/`, `basics/`, and `scanners/` subdirectories, and all tools are robustly tested against edge cases. This week transformed isolated scripts into a cohesive, production‑ready toolkit.

## Acknowledgements
Built while studying *Computer Networking: A Top‑Down Approach* (Kurose & Ross), *Python Crash Course* (Matthes), *Practical Packet Analysis (3rd ed.)* (Chris Sanders), and *The Practice of System and Network Administration* (Limoncelli).