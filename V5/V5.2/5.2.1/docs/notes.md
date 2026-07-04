# Implementation Notes

* While application frameworks (like Flask, Django, Express) offer configurations for max upload size, the **best practice** is to enforce file size limits at the reverse proxy/web server level (e.g., Nginx `client_max_body_size`, Apache `LimitRequestBody`, or AWS WAF/API Gateway).
* Enforcing it at the proxy layer drops the malicious connection before the payload even reaches your application runtime, saving CPU cycles.
* When testing locally without Nginx, setting `app.config['MAX_CONTENT_LENGTH']` in Flask is the correct approach.
