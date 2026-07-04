# Notes

- **ASVS 5.4.1 Requirement**: Verify that the application validates or ignores user-supplied filenames received through URL parameters... and always specifies a safe filename using the Content-Disposition response header.
- **Flask `send_file`**: Flask's `send_file(..., as_attachment=True, download_name=...)` automatically handles setting the `Content-Disposition` header safely. The vulnerable app manually overrides this or misuses it to demonstrate the flaw.
