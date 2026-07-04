# Solution

## Secure Implementation

The secure app:
1. Serializes the response body.
2. Encodes the body to bytes.
3. Calculates `len(body_bytes)`.
4. Sets `Content-Length` to this value.
5. Ensures declared length matches actual bytes.

Python example:

```python
body = "Hello, World!"
body_bytes = body.encode('utf-8')
content_length = len(body_bytes)
response.headers['Content-Length'] = str(content_length)
```

## Vulnerable Implementation

The vulnerable app intentionally:
1. Generates a body.
2. Sets `Content-Length` to an incorrect value.
3. Demonstrates truncation or oversizing.
4. Shows how proxies become desynchronized.

Python example (WRONG):

```python
body = "Hello, World!"
response.headers['Content-Length'] = '999'  # Incorrect!
```

## Fix for Vulnerable

Replace manual Content-Length setting with automatic calculation from the actual body length.
