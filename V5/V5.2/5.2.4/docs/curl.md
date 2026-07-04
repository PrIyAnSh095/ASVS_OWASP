# Testing with cURL

We can script cURL to test both the file count quota and the storage quota.

## 1. File Count Quota Test
```bash
echo "Tiny file" > tiny.txt
# Run 4 times in a row
for i in {1..4}; do curl -F "username=attacker" -F "file=@tiny.txt" http://localhost:5000/upload; done
```
*Secure App:* Accepts 3, rejects the 4th.

## 2. Storage Quota Test (100KB limit)
```bash
dd if=/dev/zero of=large.txt bs=1K count=150
curl -F "username=attacker2" -F "file=@large.txt" http://localhost:5000/upload
```
*Secure App:* Immediately rejects the 150KB upload because it exceeds the 100KB user quota.
