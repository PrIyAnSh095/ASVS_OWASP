# Expected Behavior

## Secure Implementation
* Maintains state for every user's uploaded files (usually via Database records: `SELECT SUM(file_size) FROM uploads WHERE user_id = ?`).
* Before accepting a new upload, calculates: `Current Storage + New File Size <= Max Quota`.
* Calculates: `Current File Count + 1 <= Max File Count`.
* If either limit is breached, the transaction is rejected gracefully.

## Vulnerable Implementation
* The user logic and upload logic are completely decoupled.
* The system accepts files until the hard drive physically runs out of space, indiscriminately impacting all users on the platform.
