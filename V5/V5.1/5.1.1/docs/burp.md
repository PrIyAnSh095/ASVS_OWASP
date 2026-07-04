# Testing with Burp Suite

Testing for documentation completeness (ASVS 5.1.1) is largely a manual review process, but Burp Suite helps verify if the backend enforces the documented policies.

## Testing Steps
1. Review the application's help pages, upload UI, or API documentation (Swagger/OpenAPI). Check for:
   * Max file size
   * Allowed extensions/MIME types
   * Malware scanning behavior
2. Use Burp Suite Repeater to upload a file exactly at the documented size limit (e.g., 2MB). It should pass.
3. Modify the payload to exceed the limit (e.g., 2.1MB). The server should reject it.
4. Attempt to upload a disallowed extension (e.g., `.php` or `.exe`). It should be rejected with a clear message referencing the policy.

## Evaluating Results
* **PASS (Secure App):** The policy is clearly documented in the UI/Docs, and the backend perfectly enforces it.
* **FAIL (Vulnerable App):** There is no documentation. The backend accepts or rejects files arbitrarily without explaining why.
