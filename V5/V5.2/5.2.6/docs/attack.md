# Attack Surface

Image uploading endpoints are vulnerable to **Pixel Flood** attacks. A Pixel Flood attack occurs when an attacker uploads an image that has a very small file size (due to high compression) but enormous pixel dimensions (e.g., 50,000 x 50,000 pixels). 

When the server attempts to decode or process this image, it allocates memory based on the image's dimensions, not its file size. A single small file can consume gigabytes of RAM, leading to memory exhaustion and Denial of Service (DoS).
