# Implementation Notes

* **Magic Bytes:** File signatures are much more reliable than extensions. Tools like `libmagic` (Python's `python-magic`) or `file` on Linux read these headers.
* **Safe Rewriting:** This is crucial. An attacker can create a file that possesses valid Magic Bytes (so it passes libmagic) but contains malicious code at the end (a Polyglot). By using a library like `Pillow` to read the image and save a *new* copy of it, you effectively sanitize the image, as the library will discard the trailing malicious code.
