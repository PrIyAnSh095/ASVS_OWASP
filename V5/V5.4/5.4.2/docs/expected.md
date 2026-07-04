# Expected Results and Pass/Fail Criteria

This document outlines the evaluation criteria for determining if an implementation meets OWASP ASVS 5.4.2 requirements.

## Evaluation Criteria Table

| Test Case | Payload | Vulnerable App (Port 5001) | Secure App (Port 5000) | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Normal Filename** | `normal.pdf` | Reflects parameter directly | Reflects parameter safely | Both download file |
| **Spaces in Name** | `report 2025.pdf` | `filename=report 2025.pdf` | `filename="report 2025.pdf"` | Secure conforms to RFC 6266 |
| **Quotes in Name** | `invoice".pdf` | Malformed header syntax | Escapes or strips double quotes | Secure preserves syntax |
| **Unicode Characters** | `résumé_✓.pdf` | Potential browser encoding errors | Employs `filename*` UTF-8 encoding | Secure preserves characters |
| **CRLF Injection** | `test%0d%0aX-Test:Injected` | Response splitting occurs (Injected Header) | CRLFs stripped or encoded | Secure blocks injection |

---

## Pass Criteria (Secure Application)
To achieve a **PASS** rating under ASVS 5.4.2:
1. **CRLF Immunity:** Carriage Return (`%0d` / `\r`) and Line Feed (`%0a` / `\n`) characters must be completely stripped or URL-encoded prior to being outputted. No header splitting must be possible.
2. **RFC 6266 Implementation:** The application must return both the standard `filename` parameter (stripped of unsafe ASCII characters, spaces, and quotes) and the advanced `filename*` parameter (formatted as `UTF-8''<url-encoded-value>`) for comprehensive compatibility.
3. **Encoding:** High-order Unicode characters, punctuation, and control characters must be URL-encoded in the `filename*` parameter to prevent layout disruption.

## Fail Criteria (Vulnerable Application)
An application **FAILS** ASVS 5.4.2 if:
1. **Unsanitized Reflection:** Input parameters are interpolated into HTTP header fields without validation.
2. **Header Injections:** Attackers can inject arbitrary headers (e.g. `Set-Cookie`, `Cache-Control`) via CRLF injection.
3. **Broken Filename Syntax:** The presence of quotes (`"`) or semicolons (`;`) in the user-supplied input breaks the structure of the `Content-Disposition` header, leading to corrupted downloads or browser errors.
