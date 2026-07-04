# Notes

- **ASVS 5.3.3 Requirement**: Verify that server-side file processing ignores user-controlled file paths inside uploaded archives to prevent Zip Slip attacks.
- Python's built-in `zipfile.extractall()` actually drops `../` and absolute paths in modern versions, acting as a built-in mitigation. However, if developers manually iterate and extract or use other libraries/OS commands (`unzip`), the vulnerability is exposed. To properly demonstrate the vulnerability and its fix manually as per ASVS requirements, the vulnerable lab mimics a manual extraction loop.
