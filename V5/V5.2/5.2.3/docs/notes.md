# Implementation Notes

* **DOCX, XLSX, APK, JAR:** Remember that many modern file formats are literally just ZIP files with a different extension. If your application parses DOCX files using a library, that library is extracting an archive under the hood and must be hardened against Zip Bombs.
* **Recursive Zip Bombs:** The most devastating zip bombs contain zip files within zip files. Standard `extractall()` doesn't inherently recurse, but if your application logic extracts an archive, then looks inside it for other archives to extract, you must track the uncompressed size globally across all recursive operations.
