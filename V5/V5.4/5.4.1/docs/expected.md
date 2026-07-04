# Expected Results

### Vulnerable Implementation
- Accepts a `filename` parameter from the query string.
- Uses the `filename` parameter directly in `os.path.join()` to locate the file on disk.
- Reflects the `filename` parameter directly into the `Content-Disposition` header.
- Allows Path Traversal to read arbitrary server files.

### Secure Implementation
- Ignores user-supplied filenames for locating files.
- Uses an internal database ID (or UUID) passed in the `id` query parameter.
- Looks up the safe internal path and original safe filename from a metadata store.
- Sets the `Content-Disposition` header explicitly using the safe, server-generated filename.
