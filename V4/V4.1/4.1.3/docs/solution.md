# ASVS 4.1.3 Solution

## Secure implementation

The secure app ignores client-supplied proxy headers and uses only internally defined trusted values.

- `X-Forwarded-For` is ignored.
- `X-Forwarded-Host` is ignored.
- `X-Forwarded-Proto` is ignored.
- `X-Real-IP` is ignored.
- `X-User-ID` is ignored.

The UI always displays the trusted values regardless of spoofed headers.

## Vulnerable implementation

The vulnerable app reads proxy headers directly from the client request.

- `Client IP` is taken from `X-Forwarded-For`.
- `User ID` is taken from `X-User-ID`.
- `Host` is taken from `X-Forwarded-Host`.
- `Protocol` is taken from `X-Forwarded-Proto`.
- `Real IP` is taken from `X-Real-IP`.

This causes the displayed behavior to change when headers are spoofed.
