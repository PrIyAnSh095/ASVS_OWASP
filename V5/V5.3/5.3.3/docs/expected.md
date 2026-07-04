# Expected Results

### Vulnerable Implementation
- Iterates over archive entries and uses `os.path.join(TARGET, entry.name)` directly.
- The `os.path.join` natively resolves `../` or absolute paths.
- Files are written outside the intended extraction folder.

### Secure Implementation
- Inspects every archive entry before extracting.
- Uses `os.path.abspath(os.path.join(TARGET, entry.name))` to resolve the final destination path.
- Verifies that the resolved absolute path starts with the absolute path of the TARGET directory.
- Rejects the archive if any entry attempts to escape the TARGET directory.
