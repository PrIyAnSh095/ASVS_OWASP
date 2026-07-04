# Theory: Public Storage vs Executable Storage

A web server (like Apache, Nginx, or IIS) relies on configurations to determine how to handle a requested file. If a directory is configured to execute scripts (e.g., passing `.php` files to the PHP-FPM processor), any file in that directory with a `.php` extension becomes a potential attack vector.

When user uploads are stored in a public directory, that directory must have execution privileges completely revoked. The web server should treat the directory purely as static data storage. Relying solely on extension blacklists during upload is insufficient because attackers constantly find bypasses. The storage configuration must act as a hard security boundary.
