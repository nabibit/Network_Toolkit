# Learning Log – Network Toolkit

This log tracks my daily progress, concepts, and artifacts.

---

## [2026-02-15] – Day 1: Binary & IP Addressing

### Concept
- **What is a network?** (Kurose 1.1–1.2): packet switching, delay, loss.
- **Binary refresher:** IP addresses are 32‑bit numbers; each octet is 8 bits.
- **OSI model:** Drew it from memory three times to internalise layers.

### Artifact
- Created `src/ip_utils.py` with `dec_to_bin` and `bin_to_dec`.
- Key decision: used `zfill(8)` to ensure 8‑bit representation – essential for future bitwise ops with subnet masks.
- Added input validation to catch errors early.

### Reflection
-  Initially forgot to strip `'0b'` from `bin()` output – now I understand why slicing is needed.
- Validation taught me to think about edge cases before they cause bugs.

### Evidence
- Code committed with message: `Add binary conversion utilities for IP octets using bin() and int()`
- Test output:
192 -> 11000000 -> 192

- **OSI Model Drawing:**  
![OSI model drawing](images/osi_drawing.png)  
*Hand‑drawn OSI model with layers and example devices.*

---
## [2026-02-16] – Day 2: IP Addressing & Subnetting Basics

### Concept
- IPv4 structure (network + host), classful vs CIDR, subnet masks.
- Subnetting formulas: network ID = IP & mask, hosts = 2^(32-mask) - 2.

### Artifact
- Extended `ip_utils.py` with:
  - `ip_to_bin()` – converts dotted decimal to 32‑bit binary.
  - `network_address()` – uses bitwise AND on binary strings.
  - `broadcast_address()` – OR with inverted mask.
  - `host_count()` – calculates usable hosts.
- Created `subnet_calculator.py` that imports these functions and prints results for a hardcoded example.

### Reflection
- Using string manipulation for bitwise ops is explicit and helps me visualise the process, though later I might switch to integer bitwise for performance.
- I solved 20 subnetting problems manually – the logic now feels solid.

### Evidence
- Code committed with message: `Add subnet calculation functions using bitwise operations`
- Packet Tracer simple LAN:
  ![Simple LAN ping](images/simple_lab.png)
- Test output:
```
IP: 192.168.1.15
Mask: 255.255.255.0
Network address: 192.168.1.0
Broadcast address: 192.168.1.255
Usable hosts: 254
```


## [2026-02-17] – Day 3: Routing, ARP & Wireshark

### Concept
- Routers forward packets between subnets; each device needs a default gateway to reach other networks.
- ARP (Address Resolution Protocol) maps IP addresses to MAC addresses on a local link.
- Wireshark can capture and filter packets (ARP, ICMP) to observe these protocols in action.

### Artifact
- Built a Packet Tracer lab with two subnets connected by a router, verified cross‑subnet ping.
- Captured ARP and ICMP traffic during a ping, saved as `arp_icmp.png`.
- Enhanced `subnet_calculator.py` with an interactive menu and loop – now the user can perform multiple calculations until they choose to quit.

### Reflection
- Watching ARP in Wireshark made the theory concrete: the first ICMP echo request triggers an ARP request for the gateway's MAC.
- The interactive menu taught me to structure user input loops robustly – checking for 'quit' at each step prevents getting stuck.
- I reused `ip_utils` functions, keeping the calculator clean and focused on UI.

### Evidence
- Packet Tracer topology:  
  ![Two subnets with router](images/two_subnets.png)
- Ping to left gateway:  
  ![Ping to 192.168.1.1](images/ping_gateway_left.png)
- Ping to right gateway:  
  ![Ping to 192.168.2.1](images/ping_gateway_right.png)
- Wireshark capture (ARP + ICMP):  
  ![ARP and ICMP packets](images/arp_icmp.png)

- Sample session:
```
=== Subnet Calculator ===
Enter IP address (e.g., 192.168.1.15): 192.168.1.15
Enter subnet mask (e.g., 255.255.255.0): 255.255.255.0

Results for 192.168.1.15 / 255.255.255.0:
Network address: 192.168.1.0
Broadcast address: 192.168.1.255
Usable hosts: 254

Another calculation? (y/n): n
Goodbye!
```

## [2026-02-18] – Day 4: TCP/UDP & Ports

### Concept
- Transport layer protocols: TCP (reliable, connection‑oriented) vs UDP (unreliable, connectionless).
- TCP three‑way handshake: SYN, SYN‑ACK, ACK.
- Port numbers multiplex connections; well‑known ports (HTTP 80, HTTPS 443, SSH 22, etc.).

### Artifact
- Wrote `tcp_client.py` – a reusable TCP client function `fetch_http()` that connects to a target, sends an HTTP GET request, and returns the response.
- Used a context manager and timeout for robustness.
- Captured a three‑way handshake on loopback (localhost) using Wireshark while connecting to a local HTTP server.

### Reflection
- Seeing the handshake in Wireshark made the theory concrete: the client sends SYN, server replies SYN‑ACK, client ACKs.
- The socket API maps directly to these steps: `connect()` triggers the handshake, `send()`/`recv()` transfer data.
- Debugging the HTTP request (initially got a 400 error) taught me to check the exact request string and line endings.

### Evidence
- Code committed with message: `Add TCP client with context manager and error handling`
- Wireshark capture of three‑way handshake on loopback:
  ![TCP three‑way handshake](images/http_handshake.png)
- Test output (local server):
```
[*] Connecting to 127.0.0.1:8000...
[+] Success. Received 2660 bytes.
Response snippet: <!DOCTYPE HTML>

<html lang="en"> <head> <meta charset="utf-8"> <title>Directory listing for /</title> </head> ...
```