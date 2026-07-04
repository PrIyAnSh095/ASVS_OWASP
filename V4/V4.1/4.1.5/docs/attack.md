# ASVS 4.1.5 Attack Document

## Message Tampering

Attackers can modify the request body in transit. Without signature verification, the server may process altered amounts or recipients.

## Request Modification

Changing fields such as `amount` or `recipient` can redirect funds or authorize unauthorized actions.

## Replay of Modified Requests

A captured legitimate request can be replayed, or replayed after modifications, to cause repeated actions.

## Man-in-the-Middle

A MITM attacker can intercept and alter unsigned or invalidly signed requests.

## Trust Boundary Violations

Once a message leaves the TLS tunnel, downstream systems must still verify integrity. TLS does not protect data after the endpoint forwards it.

## Why TLS is not enough

TLS secures the transport path, but not the message itself. Message signing ensures the payload remains valid across intermediary systems and queues.
