# Vulnerable Implementation - ASVS 5.2.2

This application fails to validate the actual content of uploaded files, relying entirely on the user-supplied filename.

## Vulnerability
Because the application only checks `filename.endswith('.jpg')`, an attacker can bypass the filter simply by renaming a malicious file. If the server later serves this file or passes it to a vulnerable backend process, it can lead to Remote Code Execution (RCE) or Cross-Site Scripting (XSS).
