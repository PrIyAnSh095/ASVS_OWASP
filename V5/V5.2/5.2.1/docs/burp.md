# Testing with Burp Suite

You can use Burp Suite to manipulate the `Content-Length` or send genuinely large payloads to test the server's limits.

## Testing Steps
1. Intercept a legitimate file upload request.
2. Send it to Repeater.
3. To generate a large payload without freezing Burp Suite, you can use Burp's "Paste from file" feature or use Python scripts to generate a massive text string in the request body.
4. Send the request to the server.

## Evaluating Results
* **PASS (Secure App):** The server immediately responds with `413 Request Entity Too Large` and drops the connection, refusing to process the massive body.
* **FAIL (Vulnerable App):** The server accepts the data. It may take a long time to upload, eventually returning a `500 Internal Server Error` as the server runs out of memory, or returning a success message after processing the massive file.
