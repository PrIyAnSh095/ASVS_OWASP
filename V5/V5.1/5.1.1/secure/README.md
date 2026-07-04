# Secure Implementation - ASVS 5.1.1

This application implements ASVS 5.1.1 by explicitly documenting the file handling policies directly in the user interface (and ideally in developer documentation).

## Implementation Details
* A clear policy lists allowed extensions (`.txt`, `.pdf`, `.png`, `.jpg`).
* It specifies the maximum file size (2 MB), which is enforced by Flask's `MAX_CONTENT_LENGTH`.
* It documents the backend behavior regarding malware scanning, informing users of what happens to malicious files.
