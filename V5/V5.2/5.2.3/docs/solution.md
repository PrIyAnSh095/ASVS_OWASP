# Solution Guide

To satisfy ASVS 5.2.3, implement pre-flight validation on all compressed formats:

1. **Python (zipfile):** Use `zf.infolist()` and check `info.file_size`.
2. **Java (java.util.zip):** Use `ZipInputStream.getNextEntry()` and track `entry.getSize()`.
3. **Node.js (yauzl):** Use the `entry` event to inspect `entry.uncompressedSize` before calling `.openReadStream()`.
4. **Limits to enforce:**
   * Max Total Uncompressed Size (e.g., 50MB)
   * Max Single File Uncompressed Size
   * Max Number of Files in the Archive
   * Max Compression Ratio (e.g., Uncompressed Size / Compressed Size > 100)
