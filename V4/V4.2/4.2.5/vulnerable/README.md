# Vulnerable Implementation - ASVS 4.2.5

This application demonstrates the vulnerable way to handle outbound HTTP requests.

## How it works

The application takes user input for the URI and various HTTP headers and directly embeds them into an outbound HTTP request using the `requests` library. It performs no length validation on these parameters. 

This is a security risk because an attacker can provide massive inputs (e.g., a 10MB authorization header), which the vulnerable server will happily allocate memory for, serialize, and transmit to the downstream service. This can lead to exhaustion of resources on the current server, the network link, or the downstream server, causing a denial of service.
