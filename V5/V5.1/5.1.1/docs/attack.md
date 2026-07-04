# Attack Vectors for ASVS 5.1.1 (Missing File Handling Documentation)

While missing documentation is not a direct exploit, it represents a severe architectural and operational vulnerability.

## The Risks of Undocumented Features
1. **Security Auditing Failures:** If developers do not explicitly document the maximum file size or allowed extensions, security testers cannot verify if the backend implementation is correct. A tester might assume a 10MB limit is intended when the business requirement was 1MB.
2. **Denial of Service (DoS):** Without documented (and enforced) limits on archive extraction sizes (e.g., zip bombs), systems are prone to CPU and disk exhaustion.
3. **Malware Handling Assumptions:** If the documentation does not explain how malware is handled, developers might assume a third-party gateway is scanning files, while the gateway assumes the application is doing it. This leads to gaps where malicious files are hosted and distributed.
