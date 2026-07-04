# Implementation Notes

* The pattern implemented in the Secure application is known as the **"Ticket-based Authentication"** or **"Connection Ticket"** pattern.
* It bridges the gap between REST (HTTP) authentication and WebSocket (TCP) persistence securely.
* A crucial part of this pattern is ensuring that tickets are **single-use** (deleted upon successful connection) and **short-lived** (e.g., 30 seconds), preventing attackers from stealing a ticket and reusing it later.
