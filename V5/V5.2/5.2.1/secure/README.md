# Secure Implementation - ASVS 5.2.1

This application securely handles file uploads by enforcing a strict maximum file size before processing the file.

## Security Control
By configuring `MAX_CONTENT_LENGTH = 1MB` in Flask, the underlying WSGI server (Werkzeug) actively monitors the incoming HTTP stream. If a client attempts to upload a file larger than 1MB, the server immediately drops the connection and returns a `413 Request Entity Too Large` error. This guarantees that large files never consume disk space or RAM, effectively preventing Denial of Service (DoS) attacks via oversized payloads.
