# Theoretical Background: Antivirus Pipelines in File Uploads

## Core Security Problem
When web systems accept files from the internet, they are accepting arbitrary data written by anonymous actors. If these files are blindly saved and served, the hosting application becomes an accomplice in malware distribution.

## Antivirus Mechanisms
Antivirus systems analyze files using two primary methodologies:

### 1. Signature-Based Detection
The scanner computes hashes or looks for specific byte-pattern sequences (signatures) matching a database of known threats.
- **Advantage:** Low false-positive rate, highly accurate for known malware.
- **Disadvantage:** Vulnerable to zero-day threats or obfuscated malware where signature hashes are altered slightly.

### 2. Heuristic Analysis
The scanner analyzes the file's structure and commands to predict if it behaves like malware.
- **Advantage:** Capable of flagging unknown variants of malware based on structural markers.
- **Disadvantage:** Higher false-positive rates.

---

## Quarantine Design Patterns
Simply running a scanner is not sufficient if the application fails to handle files safely during the scanning phase:
1. **Time-of-Check to Time-of-Use (TOCTOU):** If the application saves a file to the public downloads folder and then starts an asynchronous scan, there is a race window where users can download the file before the scanner finishes and flags it.
2. **Quarantine Isolation:** To resolve the TOCTOU issue, files must be initially saved in an isolated "Quarantine" buffer. Only when the scanning engine issues a clean response status is the file promoted (moved) to the public storage location.
