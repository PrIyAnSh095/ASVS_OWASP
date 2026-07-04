# Vulnerable Implementation

This implementation trusts user-supplied filenames for both reading and writing files, exposing the application to Path Traversal and Local File Inclusion (LFI) vulnerabilities. It violates ASVS 5.3.2.
