# Theory: Pixel Flood Attacks

An image's file size does not directly correlate with the memory required to process it. An uncompressed image typically requires `width * height * channels` bytes of memory. For example, a 10,000 x 10,000 RGB image requires approximately 300MB of RAM to decode.

Modern compression algorithms (like those in PNG and JPEG) can compress large areas of identical color into very small file sizes. An attacker can create a 50,000 x 50,000 image that is only a few kilobytes on disk but requires 7.5GB of RAM to decode. Validating only the file size fails to prevent this attack.
