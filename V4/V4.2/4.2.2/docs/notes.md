# Notes

- Content-Length calculation must happen AFTER serialization.
- Never use hardcoded or manually set Content-Length values.
- Account for character encoding (e.g., UTF-8 multibyte characters).
- Verify Content-Length during testing using Burp or curl.
- Incorrect Content-Length is a protocol violation and should be treated as a bug.
- This control applies to both requests and responses.
