# Testing with Burp Suite

Burp Suite's Intruder is the perfect tool for testing quota enforcement.

## Testing Steps
1. Intercept a legitimate file upload request.
2. Send it to Burp Intruder.
3. Clear all payloads and select "Null payloads".
4. Set the payload count to `50` (to simulate uploading the same file 50 times rapidly).
5. Start the attack.

## Evaluating Results
* **PASS (Secure App):** The first 3 requests succeed (HTTP 200). The 4th request and all subsequent requests fail (e.g., returning HTTP 403 or an HTML page showing "Quota Exceeded").
* **FAIL (Vulnerable App):** All 50 requests succeed, and the server blindly stores 50 copies of the file for a single user.
