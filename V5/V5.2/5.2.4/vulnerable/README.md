# Vulnerable Implementation - ASVS 5.2.4

This application lacks any per-user upload quotas.

## Vulnerability
While it tracks how much data a user has uploaded, it never actually enforces a limit. This allows any single user (even a newly registered, free-tier attacker account) to upload millions of files and consume terabytes of storage, leading to a complete Denial of Service via Storage Exhaustion for the entire platform.
