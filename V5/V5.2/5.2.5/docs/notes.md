# Notes

- **ASVS 5.2.5 Requirement**: Verify that the application does not allow uploading compressed files containing symbolic links unless explicitly required.
- **Python `zipfile`**: By default, `zipfile.extractall()` in Python ignores symlinks and extracts them as regular files containing the link target path as text, mitigating traditional symlink attacks *unless* the developer tries to recreate symlinks manually. However, this lab demonstrates manually preserving symlinks in the vulnerable version to show the risk, and explicitly blocking them in the secure version.
