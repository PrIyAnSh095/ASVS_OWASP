# Expected Results

### Vulnerable Implementation
- Trusts the user-supplied filename parameter directly in `os.path.join`.
- Fails to sanitize `../` or absolute paths.
- Allows an attacker to read arbitrary files from the server via the download endpoint (LFI).
- Allows an attacker to write files to arbitrary locations via the upload endpoint.

### Secure Implementation
- Generates a UUID for internal file storage. The actual file saved on disk is named `<uuid>.dat`.
- The original user-supplied filename is strictly sanitized and stored only as metadata.
- When downloading, the user requests the UUID, preventing any path traversal.
- The `werkzeug.utils.secure_filename` function is used for metadata sanitization.
