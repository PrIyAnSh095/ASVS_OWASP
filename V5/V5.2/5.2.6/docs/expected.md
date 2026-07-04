# Expected Results

### Vulnerable Implementation
- Validates only the file size (e.g., max 2MB).
- Accepts images with massive dimensions as long as the compressed file size is small.
- Fully decodes the image, risking memory exhaustion (Pixel Flood attack).

### Secure Implementation
- Reads image metadata using a trusted library (`Pillow`) without fully decoding the image contents.
- Validates that width and height are within allowed limits (e.g., max 2048x2048).
- Validates total pixel count.
- Immediately rejects any image exceeding the constraints.
