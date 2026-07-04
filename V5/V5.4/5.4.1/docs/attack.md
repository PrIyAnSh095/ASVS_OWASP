# Attack Surface

When handling file downloads, if an application relies on a user-supplied filename via URL parameters or JSON bodies to locate the file, it exposes a **Path Traversal / Local File Inclusion (LFI)** attack surface.

Furthermore, if that user-supplied filename is blindly reflected into the `Content-Disposition` response header (e.g., `Content-Disposition: attachment; filename="../../etc/passwd"`), attackers can manipulate the filename that the victim's browser uses to save the file. While modern browsers have some defenses against path traversal in the `Content-Disposition` header, reflecting unvalidated input here can still lead to spoofing the downloaded file's extension or name, tricking the user into opening a malicious file.
