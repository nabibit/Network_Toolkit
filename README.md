# Network Toolkit

A collection of Python utilities for network engineers and security students, built as part of my self‑study for the cybersecurity market.

## Current Features

- `ip_utils.dec_to_bin()` – Convert decimal octet (0–255) to 8‑bit binary.
- `ip_utils.bin_to_dec()` – Convert 8‑bit binary back to decimal.

## Installation

```bash
git clone https://github.com/bcyberly/Network_Toolkit.git
cd Network_Toolkit
# (Optional) python -m venv venv
pip install -r requirements.txt
```

## Usage Example
```bash
from src.ip_utils import dec_to_bin, bin_to_dec

print(dec_to_bin(192))   # '11000000'
print(bin_to_dec('11000000')) # 192
```

## Documentation
See docs/LEARNING_LOG.md for the detailed engineering journal.

## Acknowledgements
Built while studying *Computer Networking: A Top‑Down Approach* (Kurose & Ross)* and *Python Crash Course* (Matthes).

