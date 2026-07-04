# Notes

- **ASVS 5.2.6 Requirement**: Verify that uploaded images are rejected if their pixel dimensions exceed the application's configured maximum.
- **Library Choice**: Python's `Pillow` (PIL) library allows reading image metadata (dimensions) without loading the entire uncompressed image into memory, making it ideal for dimension validation.
