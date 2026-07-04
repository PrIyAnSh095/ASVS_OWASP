# Vulnerable Implementation

This implementation trusts user-supplied filenames from URL parameters for both file retrieval and constructing the `Content-Disposition` header, violating ASVS 5.4.1.
