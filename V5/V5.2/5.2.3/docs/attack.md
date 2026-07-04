# Attack Vectors for ASVS 5.2.3 (Zip Bombs)

Archives (like ZIP, GZ, and even DOCX, which are just ZIP files) use compression algorithms that look for repeated patterns.

## The Zip Bomb Attack
An attacker generates a file containing gigabytes of repeating zeroes. This file compresses extremely well (e.g., 10GB of zeroes compresses down to roughly 10MB).
1. The attacker uploads the 10MB ZIP. It passes the server's HTTP `Content-Length` restrictions.
2. The server blindly calls `extractall()`.
3. The server begins writing the 10GB of zeroes to the disk.
4. The server runs out of disk space, or the CPU maxes out processing the decompression, resulting in a Denial of Service.

## Inode Exhaustion
Instead of one massive file, the attacker creates an archive with 500,000 tiny 1-byte files. The extraction process creates half a million files on the filesystem, exhausting the filesystem's inodes. No further files can be created on the OS by any process.
