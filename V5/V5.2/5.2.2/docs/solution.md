# Solution Guide

To satisfy ASVS 5.2.2:

1. **Ignore Client Headers:** Never trust the `Content-Type` header provided in the HTTP request.
2. **Verify Magic Bytes:** Use a library to read the file's binary signature and determine its true MIME type.
3. **Enforce Extension Match:** Ensure the detected MIME type logically matches the uploaded extension.
4. **Sanitize via Rewriting:** For media files (images, videos), pass them through a standard processing library (like ImageMagick, Pillow, FFmpeg) to transcode or rewrite them. This destroys hidden polyglot payloads.
5. **Use Trusted Libraries:** Never write your own file parsing logic. Rely on established libraries.
