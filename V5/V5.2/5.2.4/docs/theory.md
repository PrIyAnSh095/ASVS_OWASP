# Theoretical Background - ASVS 5.2.4

Resource exhaustion is a fundamental category of Denial of Service (DoS). While Network DoS (DDoS) relies on flooding bandwidth, Application DoS relies on forcing the application to consume internal resources (Memory, CPU, Disk, Database Connections).

By failing to isolate user resources (a concept known as "Noisy Neighbor" in cloud computing), a vulnerable application allows a single malicious actor—or even just a buggy client script—to consume 100% of the shared storage pool. 

Implementing Quotas forces the application to implement "Tenant Isolation", ensuring that one user's excessive usage only impacts their own account, keeping the platform healthy for everyone else.
