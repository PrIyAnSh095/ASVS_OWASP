# Solution

To securely extract archives according to ASVS 5.3.3:

1. Determine the absolute path of the intended extraction directory.
2. For each entry in the archive, calculate the absolute path of where it would be extracted.
3. Verify that the intended extraction path `startswith()` the target extraction directory.

```python
target_dir = os.path.abspath("/tmp/uploads")
for entry in z.infolist():
    intended_path = os.path.abspath(os.path.join(target_dir, entry.filename))
    if not intended_path.startswith(target_dir + os.sep):
        raise Exception("Zip Slip detected!")
```
