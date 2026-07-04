# ASVS 4.1.1 Theory

## What is Content-Type?

The `Content-Type` header tells the client what type of data the server is sending in the HTTP response body. It is a contract between the server and the client, so the client can render or process the data correctly.

## What are MIME Types?

MIME types are standardized identifiers for media types, defined by IANA. Examples include:

- `application/json`
- `text/html`
- `application/xml`
- `text/plain`

The MIME type indicates the format of the payload and is used by browsers, APIs, and security controls.

## What is charset?

The `charset` parameter specifies the character encoding used for textual content. In modern web applications, `UTF-8` is the recommended safe default.

Example:

`Content-Type: text/html; charset=UTF-8`

Without a proper charset, the browser may use a fallback encoding or perform MIME sniffing.

## Why browsers rely on Content-Type and charset

Browsers use `Content-Type` to decide how to parse and display response data. For text-based responses, `charset` ensures that character bytes are decoded consistently. Incorrect or missing values can lead to:

- improper rendering
- garbled characters
- unsafe content interpretation

## MIME sniffing

Some browsers inspect the response body to guess the content type when the `Content-Type` header is missing or mismatched. This is called MIME sniffing.

MIME sniffing can be dangerous because it may cause a browser to execute content as the wrong type, especially if HTML or script-like content is labeled as plain text.

## Incorrect Content-Type risks

Incorrect headers can lead to:

- cross-site scripting (XSS) if HTML is treated as executable content
- mixed content rendering and security bypasses
- disclosure of sensitive data in the wrong format
- developer confusion and inconsistent behavior across clients

## Relevant RFCs and IANA Media Types

- RFC 7231: HTTP/1.1 semantics and content negotiation
- RFC 822 / RFC 2045: MIME media types
- The IANA Media Types registry defines the accepted values for `Content-Type`.

## Real-world examples

- `application/json; charset=UTF-8` for JSON APIs
- `text/html; charset=UTF-8` for HTML pages
- `application/xml; charset=UTF-8` for XML responses
- `text/plain; charset=UTF-8` for plain text

Correct header handling is a simple but critical control for safe web service behavior.
