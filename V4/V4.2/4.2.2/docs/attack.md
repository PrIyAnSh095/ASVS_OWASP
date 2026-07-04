# ASVS 4.2.2 Attack Document

## Response Desynchronization

If a proxy and backend disagree on where a response ends (due to incorrect `Content-Length`), they become desynchronized.

Example:
- Backend sends `Content-Length: 100` but body is only 50 bytes.
- Proxy reads 50 bytes (following the actual body) and then reads 50 more bytes from the next response.
- The second response is now misaligned.

## Request Smuggling via Response Confusion

A backend can intentionally send responses with incorrect `Content-Length` to:
- Cause the proxy to misinterpret subsequent messages.
- Poison the cache with malformed responses.
- Trigger request smuggling in the opposite direction (response-based).

## Proxy Confusion

A proxy facing a malformed response may:
- Truncate the response to the declared length.
- Cache only part of the response.
- Fail to update connection state correctly.
- Become desynchronized from the backend.

## Cache Poisoning

If a cache stores a response with incorrect `Content-Length`:
- Subsequent requests receive truncated or malformed content.
- The cache entry persists even after the original backend is fixed.
- Multiple users may receive corrupted responses.

## Header Manipulation

An attacker can:
- Craft a response with `Content-Length: 0`.
- Cause the proxy to ignore the actual body.
- Poison downstream caches with empty responses.

## Common Implementation Mistakes

- Hardcoding `Content-Length` without calculating actual body size.
- Forgetting to account for encoding (UTF-8 bytes vs. character count).
- Not recalculating length after serialization.
- Copying Content-Length from templates without updating.
- Manually constructing HTTP responses without validation.

## Why Incorrect Content-Length Is Dangerous

- It breaks the HTTP framing protocol.
- It causes desynchronization between endpoints.
- It enables request smuggling attacks.
- It corrupts cache entries.
- It may result in data leakage or authentication bypass.
