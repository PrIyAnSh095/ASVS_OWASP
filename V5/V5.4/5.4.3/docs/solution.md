# Solution Implementation Guide

This guide details the Python implementation demonstrating a secure Upload Antivirus pipeline.

## Implementation details

The secure lab models an enterprise workflow by separating the upload storage area into two physical directories:
1. **`quarantine/`**: Storage folder for unscanned files. Files here are never exposed to HTTP endpoints or list views.
2. **`downloads/`**: Storage folder for scanned clean files.

### Workflow Code:
```python
# 1. Save uploaded file to the quarantined area
quarantine_path = os.path.join(QUARANTINE_DIR, filename)
uploaded_file.save(quarantine_path)

# 2. Trigger scan engine
is_clean, scan_message = scan_file(quarantine_path)

if is_clean:
    # 3. Move file to clean downloads area
    destination_path = os.path.join(DOWNLOADS_DIR, filename)
    shutil.move(quarantine_path, destination_path)
else:
    # 4. Reject transaction, alert security logs, delete malicious payload
    os.remove(quarantine_path)
```

## Why this resolves ASVS 5.4.3
- **Quarantine Separation:** Even if the scanning process crashes, the file remains stuck in the quarantine directory. Since the file list view and file serving routes only look inside the `downloads/` directory, there is zero risk of serving unverified payloads.
- **Immediate Disposal:** By calling `os.remove` immediately upon threat detection, malware is purged before it can be stored permanently.
- **Log alerts:** An audit trail logging malicious uploads helps administrators block malicious IPs or user accounts.
