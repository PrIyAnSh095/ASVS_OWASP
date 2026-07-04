# Expected Behavior

## Secure Implementation
* Reads the Zip Central Directory Headers *only*.
* Tallies up the `file_size` (uncompressed size) of all entries.
* Tallies up the total number of entries.
* Rejects the file without extracting a single byte if limits are exceeded.

## Vulnerable Implementation
* Instantiates extraction directly.
* Blindly relies on the decompression library, which will faithfully execute the extraction until the OS kills the process or the disk is full.
