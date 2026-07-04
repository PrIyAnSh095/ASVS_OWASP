# Vulnerability Analysis: Header Injection / CRLF Injection

## Description
HTTP response header injection occurs when an application includes user-supplied data in an HTTP response header without proper validation, sanitization, or encoding. When an HTTP header is constructed, the standard separator between headers is a Carriage Return followed by a Line Feed sequence (`\r\n` or `%0d%0a`). 

If an attacker can inject these characters into a parameter reflected in a header (such as a custom filename in the `Content-Disposition` header), they can terminate the header line and start a new header, or even terminate the header section entirely and inject a custom HTML/script body (HTTP Response Splitting).

## Mechanism in ASVS 5.4.2 Vulnerable Lab
In the vulnerable implementation, the `filename` parameter is concatenated directly into the `Content-Disposition` header:
```python
response.headers['Content-Disposition'] = f"attachment; filename={filename_param}"
```

If a user provides:
`test%0d%0aX-Test:Injected`

The resulting HTTP headers will contain:
```http
Content-Disposition: attachment; filename=test
X-Test: Injected
```

This represents a successful HTTP Response Header Injection.

## Impact
- **Session Fixation / Cookie Injection:** Attackers can inject `Set-Cookie` headers to pre-initialize session tokens for a victim.
- **Cache Poisoning:** Injecting headers like `Cache-Control` can cause intermediate caches or CDN nodes to cache malicious content.
- **Cross-Site Scripting (XSS):** By injecting two sets of CRLF sequences, the attacker can force the header block to end and start writing the response body with execution payloads.
