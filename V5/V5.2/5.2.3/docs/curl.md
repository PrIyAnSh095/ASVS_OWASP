# Testing with cURL

Upload the test files directly using cURL:

```bash
# Upload normal file
curl -F "file=@normal.zip" http://localhost:5000/upload

# Upload file with too many items
curl -F "file=@many-files.zip" http://localhost:5000/upload

# Upload simulated Zip Bomb
curl -F "file=@simulated-zip-bomb.zip" http://localhost:5000/upload
```
