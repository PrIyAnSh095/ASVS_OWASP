# ASVS 4.2.2 Theory

## HTTP Response Structure

An HTTP response consists of:
- Status line (e.g., `HTTP/1.1 200 OK`)
- Headers (including `Content-Length`)
- Blank line (CRLF CRLF)
- Body (optional)

## Content-Length Header

The `Content-Length` header specifies the exact number of bytes in the response body.

The receiver uses this value to determine where the body ends and the next message begins.

## Message Framing

HTTP/1.1 uses headers to delimit messages. `Content-Length` is the primary framing mechanism for responses.

If `Content-Length` is incorrect:
- The receiver may read too few bytes (truncation).
- The receiver may read too many bytes (consuming part of the next message).
- Desynchronization occurs.

## Response Generation

When generating HTTP responses, the application must:
1. Serialize the response body.
2. Calculate the byte length of the serialized body.
3. Set `Content-Length` to that byte count.

Never manually set `Content-Length` to an arbitrary value.

## Reverse Proxies

Proxies and load balancers relay responses from backend servers to clients. If a backend generates an incorrect `Content-Length`, the proxy may:
- Forward the malformed response unchanged.
- Attempt to "fix" it (leading to different interpretations).
- Become desynchronized from the backend.

## Request Smuggling and Response Confusion

Response desynchronization can lead to:
- Cache poisoning (proxy caches wrong content).
- Request smuggling (client-backend desynchronization via proxy).
- Authorization bypass (wrong response reaches wrong user).

## RFC 9112

RFC 9112 (HTTP Semantics) specifies that:
- `Content-Length` must be accurate.
- Mismatched lengths are a protocol violation.
- Receivers should handle malformed lengths defensively.

## Real-world Examples

- CDNs caching responses with wrong Content-Length.
- Proxies forwarding truncated responses.
- Clients reconnecting unexpectedly due to partial responses.
- Load balancers creating request smuggling chains.
