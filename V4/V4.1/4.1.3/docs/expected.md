# Expected Results

## PASS criteria

- Trusted headers are not overridden by user-supplied values.
- Client IP remains a trusted internal value.
- User ID remains a trusted internal identity.
- Host and protocol remain trusted.
- Authorization and logging are unaffected by spoofed headers.

## FAIL criteria

- The client IP changes based on `X-Forwarded-For`.
- The user identity changes based on `X-User-ID`.
- Host changes based on `X-Forwarded-Host`.
- Protocol changes based on `X-Forwarded-Proto`.
- Audit data includes spoofed information.
