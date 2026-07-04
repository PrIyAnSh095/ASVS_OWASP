# ASVS 4.1.1 Solution

## Secure implementation

The secure Flask app sets explicit `Content-Type` headers for every response with a body.

- `/` returns HTML with `text/html; charset=UTF-8`
- `/json` returns JSON with `application/json; charset=UTF-8`
- `/html` returns HTML with `text/html; charset=UTF-8`
- `/xml` returns XML with `application/xml; charset=UTF-8`
- `/text` returns text with `text/plain; charset=UTF-8`

Every response body and header are aligned. Text-based content explicitly declares UTF-8 encoding, preventing charset ambiguity.

## Vulnerable implementation

The vulnerable application is intentionally incorrect only for ASVS 4.1.1.

- `/` returns HTML while sending `text/plain`
- `/json` returns JSON with `text/html; charset=UTF-8`
- `/html` returns HTML with `text/plain`
- `/xml` returns XML with `text/plain; charset=UTF-8`
- `/text` returns plain text but omits `charset=UTF-8`

These behaviours demonstrate mismatched MIME types, missing charset values, and generic content declarations.

## How to verify

1. Run the secure and vulnerable containers side by side.
2. Request the same endpoint on each port.
3. Compare the `Content-Type` response header to the response body.
4. The secure app passes when every type is correct and UTF-8 is specified.
5. The vulnerable app fails when the declared MIME type does not match the returned payload.
