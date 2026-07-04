# Vulnerable Implementation - ASVS 5.1.1

This application fails to document its file upload policies.

## Vulnerability
Users are presented with an upload button but given no guidance on allowed formats, file sizes, or security processes (like malware scanning). This lack of documentation makes the system unpredictable for users and makes it difficult for security engineers to audit whether the implementation matches the intended security architecture.
