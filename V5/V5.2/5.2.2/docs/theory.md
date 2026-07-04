# Theoretical Background - ASVS 5.2.2

The separation of a file's "Name" (Extension) and its "Content" (Data) is a frequent source of security vulnerabilities. Operating systems and web servers often use the extension to decide how to execute or render a file.

If an application enforces security based on the Name (e.g., "only allow .jpg"), but the web server executes based on Content, or vice versa, attackers can upload a file that passes the application's filter but is executed maliciously by the server or the end-user's operating system. 

Strictly tying the Extension, the Magic Bytes, and the actual parsed content together ensures the file is exactly what it claims to be.
