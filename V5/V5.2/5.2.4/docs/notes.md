# Implementation Notes

* **Distributed Systems:** In microservice architectures (like AWS S3 + Lambda), quota enforcement is harder because uploads might go directly to S3 via Presigned URLs. To enforce quotas in this architecture, you must issue Presigned URLs with strict byte limits, and decrement the user's remaining quota in the central database *before* issuing the URL.
* **Race Conditions:** Naive `SELECT` followed by `INSERT` quota checks are vulnerable to Time-of-Check to Time-of-Use (TOCTOU) race conditions. If an attacker sends 50 concurrent uploads, they might all pass the `SELECT` check before any `INSERT` happens, bypassing the quota. (This lab keeps it simple, but production apps should use Database Locks or Redis Atomic counters).
