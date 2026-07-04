# Testing with Burp Suite

You can use Burp Suite's Repeater or Intruder tools to test whether an application correctly limits the size of generated URIs and HTTP headers.

## Steps

1. **Capture the Request:** Intercept the form submission where you provide the target URI, Cookie, or Authorization header using Burp Suite Proxy.
2. **Send to Repeater:** Right-click the intercepted request and select "Send to Repeater".
3. **Generate a Payload:**
   * In the Repeater tab, find the parameter (e.g., `auth=Bearer+token123`).
   * Modify the value to an excessively long string (e.g., 50,000 characters of `A`). You can use Burp Suite's payload generator or simply paste a large block of text.
4. **Send the Request:**
   * In the **Secure Application**, you should receive a clean HTTP 400 Bad Request or an application-level failure message indicating the input exceeded maximum length limits. The request is never forwarded downstream.
   * In the **Vulnerable Application**, the server will attempt to process the request. It might take a long time, and you might receive an HTTP 500 error because the downstream component crashed, timed out, or returned a 414/431 error.

By generating oversized inputs, you can verify if the intermediate application is properly guarding its outbound requests.
