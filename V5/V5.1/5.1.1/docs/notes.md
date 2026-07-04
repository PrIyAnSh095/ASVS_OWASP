# Implementation Notes

* ASVS 5.1.1 is classified under "File Handling Documentation". It is a Level 1, 2, and 3 requirement.
* Documentation bridges the gap between Business Logic, Security Architecture, and User Experience.
* **Archive Files:** The requirement explicitly mentions "including unpacked size where applicable". If your application accepts `.zip` or `.tar.gz`, the documentation MUST state the maximum size of the uncompressed contents to prevent Zip Bomb attacks.
