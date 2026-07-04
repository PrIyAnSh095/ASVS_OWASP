# Vulnerable Implementation - ASVS 5.2.1

This application fails to restrict the maximum size of uploaded files.

## Vulnerability
Because there is no file size limit enforced at the framework or web server level, the application blindly accepts any upload payload. The code then attempts to read the entire file into memory (`file.read()`). An attacker can easily launch a Denial of Service (DoS) attack by uploading a multi-gigabyte file, which will exhaust the server's RAM and cause an Out of Memory (OOM) crash.

*Note: In `docker-compose.yml`, the memory is deliberately capped at 200MB to make the OOM crash easier to demonstrate locally.*
