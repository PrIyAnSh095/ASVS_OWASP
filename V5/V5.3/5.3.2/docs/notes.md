# Notes

- **ASVS 5.3.2 Requirement**: Verify that file paths are created using internally generated or trusted values instead of user-supplied filenames.
- **Python Specifics**: In Python, `os.path.join('/base/path', '/absolute/path')` evaluates to `/absolute/path`. This makes naive path joining extremely dangerous if the second argument is user-controlled.
