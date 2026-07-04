# ASVS 4.1.2 Attack Analysis

## How credentials can leak

When an API endpoint redirects HTTP traffic to HTTPS, the initial request may already contain sensitive data such as passwords, tokens, or session parameters. That first hop is visible to network attackers.

## Why redirects do not undo exposure

A redirect is only a recommendation. The original HTTP request has already been transmitted. Redirecting does not retroactively encrypt or erase the initial packet.

## Packet flow

1. Client sends `POST http://example.com/api/login` with credentials.
2. Server responds with a redirect to `https://example.com/api/login`.
3. Client follows the redirect and sends credentials again over TLS.

The attacker has already seen the first request in plaintext.

## Browser behaviour

Browsers can safely follow redirects for human-facing pages because the user can see the URL change and the path is not typically carrying sensitive API payloads.

## API behaviour

APIs are accessed by scripts and clients that should know the correct protocol. Automatic redirects change how the client is expected to behave and create a false sense of security.

## Common developer mistakes

- using a universal redirect rule for all HTTP paths
- assuming HTTPS redirects are enough for every endpoint
- tightening user-facing pages but leaving APIs on HTTP
- not rejecting HTTP requests on API routes

This lab shows how a secure implementation redirects only browser endpoints while rejecting HTTP API calls, and how a vulnerable implementation incorrectly redirects everything.
