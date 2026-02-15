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