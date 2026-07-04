# Solution

To securely store and retrieve user-uploaded files according to ASVS 5.3.2:

1. Never use the user's filename to save the file on disk.
2. Generate a random UUID and use that as the filename.
3. Keep a mapping (e.g., in a database) of the UUID to the original filename for user-display purposes.
4. If you absolutely must use the user's filename, aggressively sanitize it (e.g., stripping all path characters) using built-in framework utilities like `werkzeug.utils.secure_filename`.

```python
import uuid

# Secure file storage
internal_filename = str(uuid.uuid4())
file.save(os.path.join(UPLOAD_FOLDER, internal_filename))
```
