# Expected Behavior

## Secure Implementation
* The user interface clearly displays the allowed file extensions, maximum size, and security policies (like malware scanning) before the user selects a file.
* Developer documentation (like API specs) contains the same strict definitions.
* The backend enforces these exact documented definitions.

## Vulnerable Implementation
* The upload form provides zero context or rules.
* The backend might arbitrarily reject certain files (like `.exe`) but fails to inform the user why.
* There is no documented consensus on how large files can be or what happens if a malicious file is uploaded.
