# Notes

This lab demonstrates trust boundaries between clients and infrastructure.

- Trusted proxy headers must come from reverse proxies or load balancers.
- Clients should not be able to override headers such as `X-Forwarded-For`.
- The secure app simulates trusted values internally.
- The vulnerable app reflects spoofed values directly.

## Challenge

- Spoof `X-Forwarded-For`.
- Spoof `X-User-ID`.
- Spoof `X-Forwarded-Host`.
- Compare secure and vulnerable behavior.
- Explain why reverse proxies should inject these headers instead of clients.
