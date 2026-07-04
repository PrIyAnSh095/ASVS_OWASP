# ASVS 4.1.5 Theory

## Digital Signatures

Digital signatures prove that a message came from a trusted sender and has not been altered. In this lab we use HMAC-SHA256, which combines a shared secret with the request body.

## Message Integrity

Message integrity means the content is unchanged between sender and receiver. A signature protects against tampering.

## Authentication

HMAC ensures the request is from a party holding the shared secret. If the signature verifies, the sender is authenticated.

## Non-Repudiation

Although HMAC is symmetric and not true non-repudiation, it still provides strong assurance that the message originated from a trusted party with the shared secret.

## HMAC and SHA-256

HMAC combines a secret key with the message and hashes the result. SHA-256 is the hash function used to generate the digest.

## TLS vs Message Signing

TLS protects data in transit. Message signing protects the data itself, even if it traverses multiple intermediaries or is stored and forwarded later.

## Replay Attacks

A signed message can be replayed if no replay protections are present. This lab focuses on signature verification; production systems should also include nonces or timestamps.

## Why TLS alone is insufficient

TLS protects the tunnel, but once the message leaves that tunnel it can be modified or replayed by downstream systems. Per-message signing adds an independent integrity check.

## Real-world examples

- Banking APIs use message signatures for fund transfers.
- Payment gateways verify webhook payloads with HMAC.
- Multi-hop systems sign messages before forwarding.
