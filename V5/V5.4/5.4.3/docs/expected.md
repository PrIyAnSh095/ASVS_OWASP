# Pass/Fail Criteria for ASVS 5.4.3

This document lists the criteria required to satisfy ASVS Control 5.4.3.

## Evaluation Grid

| Scenario | Input File | Vulnerable App (Port 5001) | Secure App (Port 5000) | Compliance Result |
| :--- | :--- | :--- | :--- | :--- |
| **Normal Upload** | `clean.txt` | File made available instantly | File scanned clean and moved to downloads | both succeed (functional) |
| **Infected Upload** | `eicar.txt` | File made available instantly | File rejected, logged, and deleted | Secure passes, Vuln fails |
| **Quarantine Isolation** | Any upload | Bypasses quarantine completely | Saved to hidden `/quarantine` folder before scan | Secure passes |

---

## Secure App Compliance Verification (PASS)
To achieve a **PASS** status for ASVS 5.4.3, the system must:
1. **Enforce Quarantine Zones:** The application must write raw file uploads into a restricted directory (`/quarantine`) that is inaccessible via HTTP download routes.
2. **Mandatory AV Scanning:** Before moving files into clean storage, an antivirus engine (or simulation daemon) must evaluate the file content.
3. **Rejection & Deletion:** Any threat identification must result in aborting the transaction, printing a secure alert, logging the incident metadata, and deleting the quarantined file.

## Vulnerable App Compliance Verification (FAIL)
The application **FAILS** ASVS 5.4.3 if:
1. **Instant Exposure:** Uploaded files bypass quarantine and are immediately written to public access directories.
2. **Zero Scan Pipelines:** The system lacks verification processes to validate file contents against virus signature indexes.
3. **Persistence of Threats:** Infected payloads (like EICAR) remain stored on the server filesystem, allowing secondary users to fetch them.
