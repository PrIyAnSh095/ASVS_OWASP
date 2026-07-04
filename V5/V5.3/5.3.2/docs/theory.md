# Theory: Path Validation & Secure Generation

Relying on user input for filesystem paths is inherently dangerous. Operating systems interpret special characters like `.` (current directory), `..` (parent directory), and `/` or `\` (directory separators).

When an application attempts to append user input to a trusted base directory without validation, attackers manipulate the path resolution process. 

The gold standard for defense is an indirect reference map:
1. The server generates an opaque identifier (like a UUID).
2. The user only ever interacts with the identifier.
3. The server maps the identifier to the actual file path.

This guarantees that user input never touches filesystem APIs.
