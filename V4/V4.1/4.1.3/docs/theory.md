# ASVS 4.1.3 Theory

## Reverse Proxy and Load Balancer

A reverse proxy or load balancer sits between clients and backend servers. It can terminate TLS, route requests, and inject headers that describe the original client connection.

## Trusted Proxy Headers

Headers like `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`, `X-Real-IP`, and `X-User-ID` are often set by intermediate infrastructure.

These headers exist so the backend can learn:

- the client IP
- the original host requested by the client
- whether the client used HTTPS
- the real client IP when requests are proxied
- authenticated user identity when passed from trusted services

## Why trusting client-supplied headers is dangerous

If the backend accepts these headers directly from the client, an attacker can spoof identity, protocol, and origin. This breaks the trust boundary between client and infrastructure.

## Trust boundaries

Infrastructure-generated headers must be treated as trusted only when they come from known proxies. Clients should never be able to override these values.

## IP Spoofing and Authorization Bypass

Attackers can impersonate IP addresses or users by setting `X-Forwarded-For` or `X-User-ID`. This can bypass IP-based access controls and authorization checks.

## Audit Log Manipulation

If logs record client-supplied values instead of trusted ones, attackers can poison audit trails with false IPs or user identities.

## Real-world examples

- Web servers behind a CDN using `X-Forwarded-For`
- API gateways passing `X-Forwarded-Proto` for TLS termination
- Backend apps receiving `X-Real-IP` from a trusted proxy
- Security systems enforcing user identity based on infrastructure headers
