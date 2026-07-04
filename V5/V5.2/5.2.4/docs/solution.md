# Solution Guide

To satisfy ASVS 5.2.4:

1. **Database Tracking:** Every uploaded file must be recorded in the database, associated with a specific User ID, tracking its size in bytes.
2. **Define Quotas:** Define strict Business Logic constraints (e.g., Free Tier: 50 Files, 100MB Total; Pro Tier: 5000 Files, 10GB Total).
3. **Enforce Before Save:** Calculate the user's current utilization. If `usage + incoming_file > quota`, reject.
4. **Handle Deletions:** When a user deletes a file, ensure the storage quota is accurately decremented so they can upload again.
5. **Race Condition Prevention:** Use atomic counters in a fast data store like Redis (e.g., `INCRBY user:123:storage 50000`) or database locking to prevent concurrent quota bypasses.
