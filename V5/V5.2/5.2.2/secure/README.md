# Secure Implementation - ASVS 5.2.2

This application validates file uploads by verifying the true identity of the file, rather than trusting the user-provided filename or `Content-Type` header.

## Security Controls
1. **Extension Validation:** Basic check to ensure the extension is allowed.
2. **Magic Byte Inspection:** Uses `python-magic` (libmagic) to analyze the file's raw binary signature and derive its actual MIME type. It compares this against the expected MIME type for the given extension.
3. **Safe Rewriting:** Uses the `Pillow` library to parse images and rewrite them to a new buffer, effectively stripping out trailing malicious payloads (like PHP code appended to a valid image) or Exif metadata exploits.
