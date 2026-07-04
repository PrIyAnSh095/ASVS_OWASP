# Expected Behavior

## Secure Implementation
* The framework is explicitly configured with a maximum upload size.
* The web server actively monitors the incoming HTTP stream.
* If the stream exceeds the limit, the connection is aborted *before* the application logic parses the file.
* A clear `413 Payload Too Large` error is returned to the client.

## Vulnerable Implementation
* The server accepts the upload, allocating disk space or memory.
* The application logic triggers.
* The server runs out of resources, leading to performance degradation or a complete crash.
