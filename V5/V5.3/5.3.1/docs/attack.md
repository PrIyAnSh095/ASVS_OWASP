# Attack Surface

When applications allow users to upload files and store them in a publicly accessible directory, there is a risk of **Remote Code Execution (RCE)**. 

If an attacker uploads a file with an executable extension (e.g., `.php`, `.jsp`, `.py`) and the web server is configured to execute files with those extensions, the attacker can navigate to the uploaded file's URL and execute arbitrary code on the server.

Even if the application tries to restrict file extensions, attackers often find bypasses (e.g., `.php5`, `.pht`, `.shtml`). The most robust defense is ensuring the storage location never has execution permissions.
