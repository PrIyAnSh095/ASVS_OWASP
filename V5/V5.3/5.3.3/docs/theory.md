# Theory: Zip Slip and Path Normalization

Zip Slip is a form of directory traversal that exploits the archive extraction process. Archives preserve folder structures. An attacker manipulates this structure using Hex editors or custom scripts to embed traversal sequences.

Path Normalization is the process of resolving all `.` and `..` segments to find the true, absolute path. The only safe way to extract an archive is to normalize the combination of the target directory and the archive entry name, and strictly ensure that the resulting path is a child of the target directory.
