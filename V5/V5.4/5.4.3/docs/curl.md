# Command Line Testing with curl

We can use the `curl` utility to programmatically upload files and verify the behavior of the antivirus screening endpoints.

## 1. Uploading clean files

Create a clean sample file:
```bash
echo "This is a clean document file." > clean.txt
```

### Test Secure App (Port 5000):
```bash
curl -F "file=@clean.txt" http://localhost:5000/upload
```
**Expected Outcome:** 
The clean file is processed, accepted, and listed under downloads. Check via:
```bash
curl -s http://localhost:5000/ | grep "clean.txt"
```

---

## 2. Uploading Infected files (EICAR)

Create a sample EICAR test file:
```bash
echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.txt
```

### Test Secure App (Port 5000):
```bash
curl -F "file=@eicar.txt" http://localhost:5000/upload
```
**Expected Outcome:**
The transaction is rejected. If we list the downloads directory, `eicar.txt` will **not** be present:
```bash
curl -s http://localhost:5000/ | grep "eicar.txt"
# Result should be empty (passed)
```

### Test Vulnerable App (Port 5001):
```bash
curl -F "file=@eicar.txt" http://localhost:5001/upload
```
**Expected Outcome:**
The vulnerable application accepts the file without performing any scans. The file appears in the active file table:
```bash
curl -s http://localhost:5001/ | grep "eicar.txt"
# Result will find the file (failed)
```
