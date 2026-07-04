# curl Testing

## Fetching a Response and Inspecting Headers

```bash
curl -i http://localhost:5000/generate -X POST \
  -H "Content-Type: application/json" \
  -d '{"type":"normal"}'
```

## Understanding curl Output

The `-i` flag includes response headers:
- `Content-Length: X` — declared length
- Response body below the blank line

To measure the body:

```bash
curl -s http://localhost:5000/generate -X POST \
  -H "Content-Type: application/json" \
  -d '{"type":"normal"}' | wc -c
```

## Comparing Secure and Vulnerable

Secure (localhost:5000):

```bash
curl -i http://localhost:5000/generate -X POST \
  -H "Content-Type: application/json" \
  -d '{"type":"json"}'
```

Content-Length matches body.

Vulnerable (localhost:5001):

```bash
curl -i http://localhost:5001/generate -X POST \
  -H "Content-Type: application/json" \
  -d '{"type":"json"}'
```

Content-Length does NOT match body.

## Limitations of curl

curl automatically handles Content-Length mismatches by:
- Reading until the connection closes.
- Not strictly validating Content-Length.

For true protocol validation, use Burp Suite or a raw TCP client like `netcat` or `socat`.

## Raw TCP Testing with netcat

```bash
printf "GET /generate HTTP/1.1\r\nHost: localhost:5000\r\n\r\n" | nc localhost 5000
```

This shows the raw HTTP response, including exact byte boundaries.
