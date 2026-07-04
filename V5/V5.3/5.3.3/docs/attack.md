# Attack Surface

Archive extraction is highly vulnerable to **Zip Slip** attacks. 

Archives (like `.zip` or `.tar`) map internal files to names. If an attacker crafts an archive where a file's name contains directory traversal sequences (`../../`), a naive extraction process will append this name to the target directory. 

For example, extracting `../../etc/passwd` into `/var/www/uploads/` results in writing to `/var/www/uploads/../../etc/passwd`, which resolves to `/etc/passwd`. This leads to arbitrary file overwrite, often achieving Remote Code Execution (RCE) if a configuration or script file is overwritten.
