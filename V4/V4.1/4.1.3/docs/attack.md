# ASVS 4.1.3 Attack Analysis

## IP Spoofing

Attackers can set `X-Forwarded-For` to impersonate a trusted client IP. If the application trusts that header, access controls may allow unauthorized requests.

## Authorization Bypass

When `X-User-ID` is accepted from the client, an attacker can act as any user. This can allow access to protected resources.

## Authentication Bypass

If the backend uses a header like `X-User-ID` for identity, attackers can bypass authentication by spoofing the header.

## Audit Log Manipulation

Logging client-supplied headers can corrupt forensic evidence. Attackers can hide their real source and plant false identity data.

## Trust Boundary Violations

Headers that should be injected by proxies must not be treated as authoritative when they originate from untrusted clients. The backend must validate how the headers were set.

## Abuse of X-Forwarded-* headers

An attacker can provide arbitrary values for `X-Forwarded-For`, `X-Forwarded-Host`, and `X-Forwarded-Proto`. Vulnerable apps will then use those values for security decisions.
