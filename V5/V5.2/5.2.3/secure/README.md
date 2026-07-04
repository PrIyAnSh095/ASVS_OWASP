# Secure Implementation - ASVS 5.2.3

This application safely handles archive uploads by validating the contents *before* extraction.

## Security Controls
1. **Pre-Extraction Validation:** The `zipfile` module allows reading the central directory of the archive (`zf.infolist()`) without actually decompressing the data blocks.
2. **Uncompressed Size Limit:** We iterate through the file headers and sum `info.file_size`. If it exceeds our safety threshold (5MB), we instantly abort.
3. **File Count Limit:** We count the number of files. If an attacker submits an archive containing 100,000 empty files (Inode Exhaustion), we abort.
