# Testing with Burp Suite

Since Zip Bombs rely on specific binary file structures, Burp Suite is best used merely to deliver the payload.

## Testing Steps
1. Generate the test archives using the provided `generate_tests.py` script.
2. In Burp Suite Repeater, upload `simulated-zip-bomb.zip` (100MB uncompressed).
3. Observe the response times and status.

## Evaluating Results
* **PASS (Secure App):** The server responds almost instantly with an error: "Archive is too large when uncompressed". The server CPU/Disk usage remains stable.
* **FAIL (Vulnerable App):** The request hangs for several seconds/minutes as the server spins its CPU extracting the bomb. It may return a 500 Error if the disk fills up.
