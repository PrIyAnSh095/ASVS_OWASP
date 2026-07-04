# Solution Guide

To satisfy ASVS 5.2.1, you must prevent the application from processing oversized files.

1. **Framework Limits:** Configure your framework to reject large requests globally or per-route.
   * **Flask:** `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024`
   * **Express (Multer):** `multer({ limits: { fileSize: 1000000 } })`
   * **Spring Boot:** `spring.servlet.multipart.max-file-size=10MB`
2. **Reverse Proxy Limits (Recommended):** Block large requests at the edge.
   * **Nginx:** Add `client_max_body_size 10M;` to the server block.
3. **Avoid In-Memory Processing:** Never use methods like `.read()` or `.getBytes()` on uploaded files unless you are absolutely certain the size limit is enforced. Use streaming APIs to process files in chunks.
