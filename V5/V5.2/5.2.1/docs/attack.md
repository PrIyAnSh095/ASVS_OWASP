# Attack Vectors for ASVS 5.2.1 (Oversized Files)

Failing to restrict file upload sizes opens the server to severe Resource Exhaustion and Denial of Service (DoS) attacks.

## The Attack
1. **Memory Exhaustion (OOM):** If an application reads uploaded files directly into RAM (e.g., to parse a CSV, resize an image, or calculate a hash), an attacker uploading a 5GB file will instantly consume 5GB of the server's RAM. If the server has less RAM available, the process crashes.
2. **Disk Exhaustion:** Even if the framework safely spools large uploads to temporary disk files (like Flask does by default for large files), an attacker can script thousands of concurrent 10GB uploads, rapidly filling the server's hard drive and taking down the entire database/OS.
3. **Bandwidth Exhaustion:** Large file uploads monopolize network connections and worker threads.
