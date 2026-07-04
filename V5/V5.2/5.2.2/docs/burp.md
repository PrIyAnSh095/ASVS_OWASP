# Testing with Burp Suite

Burp Suite allows you to easily bypass front-end extension checks and manipulate the `Content-Type` header to test backend validation.

## Testing Steps
1. Create a dummy script file containing `<?php echo "Test"; ?>`. Save it as `shell.php`.
2. Intercept the file upload request.
3. In Burp Repeater, change `filename="shell.php"` to `filename="shell.jpg"`.
4. Change the `Content-Type` to `image/jpeg`.
5. Send the request.

## Evaluating Results
* **PASS (Secure App):** The server analyzes the binary content, sees the text (text/x-php), notices it doesn't match the `.jpg` extension expectation, and rejects it with an error.
* **FAIL (Vulnerable App):** The server looks at `.jpg`, ignores the actual content, and blindly saves the file.
