# Notes

This lab focuses on protocol handling, not TLS implementation. Students should understand that:

- browser redirects are acceptable for user-facing pages
- APIs must not transparently redirect from HTTP to HTTPS
- the first HTTP API request may already expose sensitive data
- a redirect does not retroactively protect the original request

## Screenshot guidance

Capture these screenshots:

- Network tab showing `http://localhost:5000/` returning `302` to `https://localhost:5000/`
- Network tab showing `http://localhost:5000/api/profile` returning `403` with no `Location`
- Network tab showing `http://localhost:5001/api/login` returning `307` with `Location: https://localhost:5001/api/login`

These screenshots should illustrate the secure versus vulnerable behavior clearly.
