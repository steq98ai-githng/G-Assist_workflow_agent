# Security Policy

## Supported Versions

Currently, only the latest release (v4.0.4+) of the System Workflow Agent is supported for security updates.

| Version | Supported          |
| ------- | ------------------ |
| >= 4.0.4| :white_check_mark: |
| < 4.0.0 | :x:                |

## Secret Management
* **API Keys:** The Gemini API key must never be hardcoded. It is loaded via the `GEMINI_API_KEY` environment variable or read from `gemini-api.key` stored securely in the plugin's data directory.
* **Paths:** Do not use hardcoded absolute paths to user home directories. Always use environment variables (`PROGRAMDATA`) or dynamic path resolution.

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please report it via a private GitHub issue or contact the maintainers directly. Do not disclose vulnerabilities publicly until they have been patched.
