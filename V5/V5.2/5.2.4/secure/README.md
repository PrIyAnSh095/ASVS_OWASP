# Secure Implementation - ASVS 5.2.4

This application securely implements per-user quotas for file uploads.

## Security Controls
1. **File Count Enforcement:** The server tracks how many files `user1` has uploaded. If the count exceeds the configured limit (3), the server rejects the request.
2. **Storage Quota Enforcement:** The server tracks the total bytes `user1` is storing. If uploading a new file would push the user's total usage over their limit (100 KB), the upload is rejected.
3. **Prevention of Resource Exhaustion:** By binding storage directly to an authenticated user's identity, an attacker cannot write scripts to loop and fill the server's hard drive infinitely.
