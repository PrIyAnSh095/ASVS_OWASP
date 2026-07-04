# Theory: Content-Disposition and File Downloads

The `Content-Disposition` HTTP header instructs the browser on how to display the response.
- `inline`: Display in the browser (e.g., viewing a PDF).
- `attachment`: Prompt the user to save the file to disk.

The `filename` directive within the header (e.g., `Content-Disposition: attachment; filename="report.pdf"`) suggests a default save name.

If this header relies on unvalidated user input, attackers can control the suggested filename. Combined with a Path Traversal vulnerability in the file fetching logic, an attacker can both read arbitrary files and spoof the downloaded filename presented to the user.
