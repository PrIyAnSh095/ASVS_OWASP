# Attack Vectors for ASVS 5.2.2 (Improper File Validation)

When an application relies solely on the filename extension or the `Content-Type` header (which is entirely controlled by the user), it becomes vulnerable to multiple file-based attacks.

## Polyglots and Disguised Files
1. **Renamed Executables:** An attacker renames an executable to `invoice.pdf`. If a downstream user downloads it and their OS hides file extensions, they might execute it.
2. **Web Shells:** An attacker uploads a PHP script renamed to `shell.jpg`. If the web server is misconfigured (e.g., Apache `AddHandler` misconfigurations), accessing `shell.jpg` might execute the PHP code.
3. **Image Polyglots:** An attacker creates a valid JPG file, but appends a script payload to the end of the binary data. The vulnerable app accepts it because the extension is `.jpg`. If the server is tricked into executing it, the valid image header is ignored, and the trailing script is executed.
