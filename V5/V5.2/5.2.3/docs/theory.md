# Theoretical Background - ASVS 5.2.3

Compression algorithms are designed to trade CPU cycles for storage efficiency. In the context of a web server, an attacker weaponizes this efficiency. 

Because the web server's initial defense (`Content-Length` validation) only sees the highly efficient compressed size, the payload easily bypasses size restrictions. Once the payload crosses the threshold into the application logic, the decompression engine unpacks it into its true form, overwhelming the host infrastructure. 

Pre-flight inspection of archive headers is the only effective defense.
