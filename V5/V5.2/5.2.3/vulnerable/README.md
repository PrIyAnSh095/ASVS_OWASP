# Vulnerable Implementation - ASVS 5.2.3

This application is highly vulnerable to Archive Bombs (Zip Bombs).

## Vulnerability
The server calls `zf.extractall()` immediately on any valid ZIP file uploaded. An attacker can craft a 42-kilobyte ZIP file that decompresses into 4.5 Petabytes of data (e.g., the infamous 42.zip). When the server attempts to extract this, it will consume 100% of the CPU and rapidly fill the entire hard drive, causing a complete Denial of Service.
