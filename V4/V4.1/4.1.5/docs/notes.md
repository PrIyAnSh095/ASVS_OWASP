# Notes

- The secure implementation validates HMAC-SHA256 signatures on every sensitive POST endpoint.
- The vulnerable app processes requests regardless of the signature state.
- Students should observe that message signing is separate from TLS.
- This lab demonstrates why sensitive transactions require per-message integrity protection.
