# Expected Results

### Vulnerable Implementation
- Uploads any ZIP archive without checking its entries.
- Symlinks are preserved during extraction (if OS/Python `zipfile` allows, or custom extraction).
- If the attacker downloads/reads the extracted symlink, they get arbitrary file read.

### Secure Implementation
- Inspects every `ZipInfo` entry in the archive before extraction.
- Checks if the entry attributes indicate a symbolic link.
- Rejects the entire archive if any symlink is found, returning a validation error.
