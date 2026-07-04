# Solution

To implement a secure archive upload regarding ASVS 5.2.5:

1. Open the archive but **do not** extract it immediately.
2. Iterate through all entries.
3. For ZIP files, check the `external_attr` of each `ZipInfo` object.
4. If `(info.external_attr >> 16) & 0o120000 == 0o120000`, the entry is a symlink.
5. Reject the archive.

```python
for info in z.infolist():
    if stat.S_ISLNK(info.external_attr >> 16):
        raise ValueError("Symlinks not allowed")
```
