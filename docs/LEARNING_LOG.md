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