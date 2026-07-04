# Theoretical Background - ASVS 5.2.1

File uploads are fundamentally dangerous because they hand control over server resources directly to the end-user. 

When an HTTP request containing a file is sent, the server must buffer that request somewhere (memory or disk) before the application can parse the multipart form data and extract the file. If there are no limits, an attacker controls exactly how much memory or disk space the server consumes.

ASVS 5.2.1 targets the most basic layer of defense: ensuring the application explicitly defines and enforces what a "safe size" means for its specific business context.
