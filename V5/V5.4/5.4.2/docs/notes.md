# Engineering Notes: Safe Filename Handling in HTTP Headers

## Overview
Filenames returned in HTTP response headers (such as `Content-Disposition`) represent a significant integration boundary. Unlike typical HTML response bodies where HTML entity encoding is the standard defense, headers require strict adherence to HTTP protocol specifications. 

## Protocol Constraints
The `Content-Disposition` header structure is defined in RFC 6266. It consists of:
1. A disposition type (typically `inline` or `attachment`).
2. Parameters separated by semicolons.
3. The `filename` parameter (which only supports ASCII characters, and expects double-quoted values if spaces are present).
4. The `filename*` parameter (defined in RFC 5987, which supports full Unicode via a specific encoding: `UTF-8''` followed by the URL-encoded filename).

## Key Vulnerability Mechanisms

### 1. HTTP Response Splitting & CRLF Injection
In HTTP/1.1, the headers block is separated from the body by double CRLF (`\r\n\r\n`). Each header is separated by a single CRLF (`\r\n`). If a server prints a filename that contains `\r\n`, the HTTP parser on the client (or reverse proxy) will interpret the subsequent bytes as new headers, leading to critical injection attacks.

### 2. Header Value Truncation & Corruption
Characters such as semicolons (`;`), double quotes (`"`), and equal signs (`=`) have specific semantic meaning inside HTTP headers. If an attacker inputs:
`filename="report; type=text/html; version="`

It can corrupt the parsed parameters in the browser, causing it to misinterpret the file type or download path.

### 3. Unicode Handling Issues
If a filename contains characters like standard accents or emojis, sending them in raw ISO-8859-1 or UTF-8 without proper RFC 5987 structure can result in either character corruption ("mojibake") or server failures, depending on the underlying framework.

## Defense Strategy
1. **CRLF Elimination:** Globally strip `\r` and `\n` from any input that is bound for an HTTP header.
2. **Double Parameter Standard:** Provide both `filename` (for backwards compatibility with older clients, with non-ASCII stripped) and `filename*` (conforming to RFC 6266 format).
3. **URL Encoding:** Always URL-encode the UTF-8 representation of the filename when populating the `filename*` parameter.
