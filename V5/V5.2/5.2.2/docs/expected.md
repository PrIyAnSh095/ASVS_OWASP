# Expected Behavior

## Secure Implementation
* Reads the first few bytes of the file (Magic Bytes / File Signature) to determine its true MIME type (e.g., `FF D8 FF E0` for JPEG).
* Asserts that the detected MIME type matches the permitted list *and* matches the provided extension.
* For complex formats (Images, PDFs), it safely parses and rewrites the content using a trusted library (e.g., `Pillow` for Python) to strip out polyglot payloads.

## Vulnerable Implementation
* Splits the string filename by `.` and checks the last element against a hardcoded list.
* Implicitly trusts the `Content-Type` header sent by the HTTP client.
* Saves the raw byte stream directly to the disk without rewriting or scanning it.
