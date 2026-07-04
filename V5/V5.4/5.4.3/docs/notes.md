# Engineering Notes: Antivirus Integrations and Quarantine Workflows

## Antivirus Architectures
In high-security enterprise systems, web application nodes should not execute file processing internally. Instead, a decoupled architecture is utilized to isolate untrusted user data.

### 1. ClamAV Integration (Daemon Mode)
ClamAV is a widely used open-source antivirus engine. Instead of running the `clamscan` CLI utility (which has a high startup latency because it must load database definitions into memory for every call), production systems use `clamd` (the ClamAV daemon). 

Communications occur over a TCP socket or Unix Domain Socket:
- The Flask app sends an `INSTREAM` command to ClamAV.
- The file stream is piped over the network.
- ClamAV returns a string containing `stream: OK` or `stream: <virus_name> FOUND`.

### 2. S3/Cloud Storage Workflows
In modern cloud architectures:
- Uploads are directed to an isolated "Quarantine S3 Bucket".
- An upload event triggers a serverless function (e.g., AWS Lambda) containing the antivirus package (e.g. ClamAV running inside containerized Lambdas).
- If clean, the lambda function copies the file to the "Public Downloads Bucket".
- If infected, the Lambda triggers an alert and moves the file to an archival forensics bucket.

## Key Design Principles
1. **Never Execute Uploaded Files:** Quarantined directories must be configured with execution permissions disabled (`noexec` mount flag).
2. **Deterministic Purging:** Purge the quarantine folder periodically using automated cron tasks to prevent storage leaks from aborted or failed scans.
3. **Defense-in-Depth:** In addition to antivirus scanning, enforce file size limits, whitelist extensions, and strip metadata (e.g., EXIF headers in images) to prevent alternate attack vectors.
