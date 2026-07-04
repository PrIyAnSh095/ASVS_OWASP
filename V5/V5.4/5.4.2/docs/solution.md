# Solution Implementation Guide

This document describes the secure implementation of filename handling in Flask for ASVS 5.4.2.

## Secure Filename Handler Algorithm

The secure implementation contains a specialized filename encoder that handles ASCII fallbacks, URL encoding, and CRLF protection.

### Implementation in Python (Flask)

```python
import re
from urllib.parse import quote

def make_safe_content_disposition(filename_param):
    # Step 1: Strip carriage returns and line feeds to prevent CRLF injection
    sanitized_filename = re.sub(r'[\r\n]', '', filename_param)
    
    # Step 2: Create a safe ASCII-only fallback filename
    # Strip double quotes and backslashes to avoid header syntax injection
    ascii_safe_filename = sanitized_filename.encode('ascii', errors='ignore').decode('ascii')
    ascii_safe_filename = ascii_safe_filename.replace('"', '').replace('\\', '_')
    if not ascii_safe_filename.strip():
        ascii_safe_filename = "download.pdf"
        
    # Step 3: URL-encode the UTF-8 version for modern browsers (RFC 5987 / 6266)
    utf8_encoded_filename = quote(sanitized_filename)
    
    # Step 4: Construct the final header value
    content_disposition = f"attachment; filename=\"{ascii_safe_filename}\"; filename*=UTF-8''{utf8_encoded_filename}"
    
    return content_disposition
```

## Why this is Secure

1. **Deterministic CRLF Mitigation:** The application uses regex (`[\r\n]`) to strip control characters before they can reach the server's response headers.
2. **Dual-Format Safety:** 
   - The classic `filename="..."` attribute is wrapped in quotes, and internal quotes are removed. This prevents an attacker from escaping the quotes to inject parameters like `filename="a"; parameter="b"`.
   - The modern `filename*="..."` attribute is fully URL-encoded (Percent-Encoded), which is safe by design because characters like spaces, semicolons, and quotes are converted to hex codes (`%20`, `%3B`, `%22`), stripping them of special meaning.
3. **No Unrelated Open Handlers:** Path traversal is separately handled using `werkzeug.utils.safe_join` to prevent users from downloading system files.
