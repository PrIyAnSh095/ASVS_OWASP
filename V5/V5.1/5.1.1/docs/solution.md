# Solution Guide

To satisfy ASVS 5.1.1:

1. **Write a File Upload Policy:** Create a standardized document or UI component that lists:
   * Permitted file extensions (e.g., `.jpg`, `.pdf`).
   * Permitted MIME types.
   * Maximum file size (e.g., 5 MB).
   * Maximum unpacked size (if archives are allowed).
2. **Document Malware Handling:** Explicitly state the system's behavior when malware is detected (e.g., "Files are scanned by ClamAV. Infected files are deleted and administrators are alerted.").
3. **Align Backend:** Ensure the backend code (e.g., Flask's `MAX_CONTENT_LENGTH`) exactly matches the documented numbers.
4. **API Documentation:** If building an API, include these limits in the OpenAPI/Swagger specification under the schema definition for the file upload endpoint.
