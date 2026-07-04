# Theory: Symlink Attacks

A symbolic link is a file that points to another file or directory. Archive formats like ZIP and TAR support storing symlinks.

If a web application extracts a symlink `link.txt -> /etc/passwd`, the operating system will resolve `link.txt` to `/etc/passwd`. 
If the application later serves `link.txt` back to the user, the attacker can read sensitive system files.

To defend against this, applications must inspect archive contents and reject symlinks, or ensure they only point to approved locations (allowlisting).
