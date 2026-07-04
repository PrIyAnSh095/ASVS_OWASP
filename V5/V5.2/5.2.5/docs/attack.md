# Attack Surface

Uploading archives is dangerous because extraction logic often assumes the archive's internal paths are benign. 
In ASVS 5.2.5, we focus on **Symbolic Links (Symlinks)** inside archives.

If the application extracts an archive without checking for symlinks, an attacker can include a symlink pointing to a sensitive file outside the target directory (e.g., `/etc/passwd`). 
When the backend reads or modifies the extracted file, it inadvertently reads or modifies the target of the symlink.

This is different from Zip Slip, where the filename itself contains directory traversal sequences (`../../`). Symlink attacks rely on the filesystem features embedded in the archive format.
