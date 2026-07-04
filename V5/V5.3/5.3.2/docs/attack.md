# Attack Surface

When applications use user-supplied filenames directly in filesystem operations (like opening, saving, or deleting files), they expose themselves to **Path Traversal** and **Local File Inclusion (LFI)** vulnerabilities.

An attacker can supply a filename like `../../../etc/passwd` or `..\..\windows\system32\drivers\etc\hosts`. If the backend merely concatenates this input with a base directory (e.g., `os.path.join(UPLOAD_DIR, user_input)`), the operating system resolves the `../` sequences, allowing the attacker to read, write, or overwrite files outside the intended directory.

If absolute paths are provided (e.g., `/etc/passwd`), many programming languages (including Python's `os.path.join`) will discard the base directory and write directly to the absolute path, compounding the risk.
