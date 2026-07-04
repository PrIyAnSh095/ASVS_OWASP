# Expected Results

## PASS criteria

| Endpoint | Expected Content-Type | Expected charset | Notes |
| --- | --- | --- | --- |
| `/` | `text/html; charset=UTF-8` | `UTF-8` | HTML body matches header |
| `/json` | `application/json; charset=UTF-8` | `UTF-8` | JSON body matches header |
| `/html` | `text/html; charset=UTF-8` | `UTF-8` | HTML body matches header |
| `/xml` | `application/xml; charset=UTF-8` | `UTF-8` | XML body matches header |
| `/text` | `text/plain; charset=UTF-8` | `UTF-8` | Plain text body matches header |

## FAIL criteria

| Failure type | Example behaviour | Why it fails |
| --- | --- | --- |
| Wrong MIME Type | `JSON` served as `text/html` | Content does not match advertised type |
| Missing charset | `text/plain` without `charset=UTF-8` | Text encoding is unspecified |
| Generic MIME Type | `text/plain` for XML or JSON | Response is too broad; browser may misinterpret it |
| Mismatched response | HTML body with `application/json` | Body and header conflict |

## What PASS looks like

- The response contains an explicit `Content-Type` header.
- The MIME type accurately describes the response body.
- The header includes `charset=UTF-8` for text-based payloads.
- The response body renders or parses correctly.

## What FAIL looks like

- The `Content-Type` header is incorrect for the returned body.
- The `charset` parameter is omitted for text or HTML.
- The header is generic or inconsistent with the payload.
- The browser or client may interpret the response incorrectly.
