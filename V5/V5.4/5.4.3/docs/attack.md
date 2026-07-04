# Malware Threats in File Uploads

## Overview
Web applications that accept file uploads from users (e.g. resumes, profile pictures, documents) open a significant attack surface. If these files are stored directly on the server filesystem and made accessible to other users, the application can act as a distribution vector for malware, viruses, ransomware, and malicious scripts.

## Attack Scenarios

### 1. Malware Distribution
An attacker uploads a malware payload (e.g., a Trojan or ransomware wrapper) named `invoice.pdf.exe`. If the web server lacks scanning, other users downloading files from the platform will receive the payload. This damages the reputation of the organization hosting the site and compromises its users.

### 2. EICAR Test File Simulation
To safely test whether an antivirus program or gateway scanner is active, the European Institute for Computer Antivirus Research (EICAR) created a standardized 68-byte printable ASCII string. Any compliant antivirus engine will identify this string as a signature match for a test virus, rejecting or quarantining the file immediately.

The string is:
`X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*`

## The Danger of Untrusted Files
Files uploaded from unauthenticated or untrusted users must never be trusted. They should be considered hostile by default. Without automated antivirus pipelines:
- Attackers can target downstream processing tools (e.g. PDF parsers, image conversion libraries) by uploading files designed to trigger Remote Code Execution (RCE) via parsing bugs (e.g., ImageTragick).
- Ransomware can be propagated across internal shared drives.
