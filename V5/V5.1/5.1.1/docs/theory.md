# Theoretical Background - ASVS 5.1.1

Security by obscurity does not work for file uploads. A robust security posture requires "Secure by Design," which starts with clear documentation.

When an application's file upload constraints are undocumented:
1. **Users get frustrated** because their files are rejected with generic "Upload Failed" messages.
2. **Developers make mistakes** because they don't know the intended constraints when refactoring or migrating the backend.
3. **Security analysts cannot audit** the application effectively because there is no baseline "truth" to test against.

By enforcing strict documentation (ASVS 5.1.1), organizations ensure that everyone understands the boundaries of the upload feature, making it significantly easier to implement the technical controls (like ASVS 5.1.2 and 5.1.3) correctly.
