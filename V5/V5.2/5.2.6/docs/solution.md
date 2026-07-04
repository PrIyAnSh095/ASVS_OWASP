# Solution

To securely handle image uploads according to ASVS 5.2.6:

1. Validate the file size as a basic measure.
2. Open the image using a library that supports reading metadata without decoding the full image (e.g., `PIL.Image.open`).
3. Check the `width`, `height`, and `width * height` (total pixels).
4. Reject the image if it exceeds the configured thresholds.

```python
from PIL import Image

MAX_WIDTH = 2048
MAX_HEIGHT = 2048
MAX_PIXELS = MAX_WIDTH * MAX_HEIGHT

img = Image.open(file_stream)
if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
    raise ValueError("Dimensions too large")
```
