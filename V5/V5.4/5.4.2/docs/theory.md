# Theoretical Background: ASVS 5.4.2 & RFC 6266

## Core Concepts

### Content-Disposition Header
The `Content-Disposition` header is an HTTP response header that tells the browser whether to display the response inline in the browser window, or to download it locally as an attachment.

Syntax:
`Content-Disposition: attachment; filename="filename.jpg"`

### RFC 6266
RFC 6266 is the formal specification defining the use of the `Content-Disposition` header in HTTP. It standardizes how filenames should be returned, especially when dealing with non-ASCII characters.

Because HTTP headers historically only supported ISO-8859-1 (Latin-1) characters, browsers handled Unicode filenames inconsistently, often leading to corrupted filenames or server crashes. RFC 6266 solves this by introducing the `filename*` parameter, which leverages RFC 5987 encoding:

`Content-Disposition: attachment; filename="fallback.txt"; filename*=UTF-8''%e2%9c%93%20unicode.txt`

## The Vulnerability: Response Header Injection

If user input is directly concatenated into the header string:
`filename = user_input`

An attacker can exploit this in two main ways:

### 1. Parameter Injection (RFC Violation)
By injecting a semicolon or quotes, the attacker can break the structural parsing of the header:
`filename="test.txt"; modification-date="2026-01-01"`
This allows them to spoof metadata or cause parsing errors in the browser.

### 2. HTTP Response Splitting / CRLF Injection
HTTP messages use CRLF (`\r\n`) to demarcate headers. If user-controlled data containing raw `\r\n` is placed inside the header block, the HTTP parser interprets the carriage return and line feed as the end of the current header line and the beginning of a new one.

This enables attackers to inject arbitrary headers, such as:
- `Set-Cookie`: To perform session fixation.
- `Location`: To force open redirects.
- `Content-Type`: To override the MIME type and execute scripts.
- Custom body: By injecting two CRLF sequences, the attacker terminates the header block entirely and writes a custom body payload, which leads to XSS.
