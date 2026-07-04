# Attack Vectors for ASVS 5.2.4 (Quota Exhaustion)

Unrestricted uploads lead directly to Resource Exhaustion.

## The "Free Tier" DoS Attack
1. An attacker registers a free account.
2. The attacker writes a simple Python loop that repeatedly uploads a 1MB file to the server.
3. Because the server only limits the *individual* file size (e.g., 5MB max), each individual upload succeeds.
4. Over a weekend, the attacker's script successfully uploads 500,000 files, consuming 500 GB of the server's hard drive.
5. The database crashes, OS logs cannot write, and legitimate users can no longer upload avatars or documents.

## Inode Exhaustion
An attacker can upload millions of 1-byte files. The hard drive might have 1TB of free space remaining, but the filesystem runs out of "inodes" (file pointers). The entire OS halts because it can no longer create any files. Enforcing a Maximum File Count quota prevents this.
