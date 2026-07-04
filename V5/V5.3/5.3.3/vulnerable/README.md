# Vulnerable Implementation

This implementation naively extracts archive entries without validating if the resolved path escapes the intended extraction directory, exposing it to Zip Slip attacks. It violates ASVS 5.3.3.
