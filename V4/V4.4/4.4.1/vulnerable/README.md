# Vulnerable Implementation - ASVS 4.4.1

This application uses unencrypted WebSockets (`ws://`).
Because it lacks Transport Layer Security (TLS), all messages sent between the client and the server can be intercepted and read in plain text by anyone monitoring the network traffic (e.g., via Wireshark or a Man-in-the-Middle attack).
