# Implementation Notes

* In a production environment, you typically do not configure SSL directly in the Python application (as done in the secure lab using `ssl_context='adhoc'`).
* Instead, WebSockets run behind a reverse proxy or load balancer (like NGINX, HAProxy, or AWS ALB) which terminates the TLS connection. 
* To satisfy ASVS 4.4.1 in that architecture, you must configure the load balancer to redirect HTTP to HTTPS, and ensure that the frontend explicitly requests `wss://`. Additionally, the backend can check the `X-Forwarded-Proto` header to ensure the outer connection was secure.
