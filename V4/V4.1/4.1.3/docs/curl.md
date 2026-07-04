# curl Verification

## Secure lab
curl -i http://localhost:5000/ \
  -H "X-Forwarded-For: 127.0.0.1" \
  -H "X-Forwarded-Host: attacker.example.com" \
  -H "X-Forwarded-Proto: https" \
  -H "X-Real-IP: 10.0.0.1" \
  -H "X-User-ID: admin"

Expected:
- Secure app still shows trusted values.
- `Client IP` remains `10.0.0.10`.
- `User ID` remains `proxy-user-42`.
- `Host` remains `secure.example.com`.
- `Protocol` remains `https`.

## Vulnerable lab
curl -i http://localhost:5001/ \
  -H "X-Forwarded-For: 127.0.0.1" \
  -H "X-Forwarded-Host: attacker.example.com" \
  -H "X-Forwarded-Proto: https" \
  -H "X-Real-IP: 10.0.0.1" \
  -H "X-User-ID: admin"

Expected:
- Vulnerable app shows spoofed values.
- `Client IP` changes to `127.0.0.1`.
- `User ID` changes to `admin`.
- `Host` changes to `attacker.example.com`.
- `Protocol` changes to `https`.
