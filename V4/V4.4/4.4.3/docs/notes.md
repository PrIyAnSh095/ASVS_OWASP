# Implementation Notes

* **Why Dedicated Tokens?** If your WebSocket server is hosted on a different domain than your frontend (e.g., `api.example.com` vs `www.example.com`), `HttpOnly` session cookies might not be sent automatically during the WebSocket handshake due to CORS/SameSite restrictions. In these cases, dedicated connection tokens (like Connection Tickets) are strictly required.
* **One-Time Use:** Ideally, a dedicated WebSocket token should be a one-time use "ticket". The client requests a ticket via an authenticated HTTP REST call, receives a ticket valid for 30 seconds, uses it to open the WebSocket, and the server immediately burns the ticket.
