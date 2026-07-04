# Burp Suite Verification

## 1. Capture a request

- Configure Burp proxy.
- Open `http://localhost:5000/` for the secure lab, or `http://localhost:5001/` for the vulnerable lab.
- Capture the request in Proxy > HTTP history.

## 2. Send to Repeater

- Right-click the request and select `Send to Repeater`.
- In Repeater, edit the request headers.

## 3. Add spoofed headers

- `X-Forwarded-For: 127.0.0.1`
- `X-Forwarded-Host: attacker.example.com`
- `X-Forwarded-Proto: https`
- `X-Real-IP: 10.0.0.1`
- `X-User-ID: admin`

## 4. Observe behaviour

### Secure
- The displayed values remain the trusted internal values.
- No user-supplied header changes the detected identity or protocol.

### Vulnerable
- The displayed values change based on the spoofed headers.
- The application uses `X-User-ID`, `X-Forwarded-For`, and other headers directly.
