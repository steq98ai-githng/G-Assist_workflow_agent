## 2025-05-14 - License Transition to Apache 2.0

**Vulnerability:** N/A (Compliance/Legal update)

**Learning:** When transitioning licenses, it is critical to search for all occurrences of the old license in documentation, manifests, and source code headers (SPDX identifiers).

**Prevention:** Use automated scripts to verify license headers across the repository.

## 2026-05-01 - User Query Length Validation

**Vulnerability:** Resource Exhaustion & Prompt Injection Risk

**Learning:** To prevent resource exhaustion and mitigate certain prompt injection attacks (e.g., extremely long queries designed to overwhelm the model or sandbox), user input must be validated against a reasonable length limit before being processed by the LLM. This limit should be grounded in the system's overall message size constraints.

**Prevention:** Implement a `MAX_QUERY_LENGTH` (e.g., 10,000 characters) check at the entry point of query processing and return a clear, actionable error message to the user if the limit is exceeded.

## 2026-05-02 - Subprocess Injection in MCP Client

**Vulnerability:** Subprocess Injection Risk

**Learning:** MCP server initialization using `StdioTransport` takes a command and arguments from the configuration. If these are not validated, an attacker who can modify the configuration could execute arbitrary shell commands by including shell metacharacters.

**Prevention:** Validate all parts of the subprocess command and arguments against a blacklist of forbidden shell metacharacters (e.g., `;`, `&`, `|`, `$`, `` ` ``) before spawning the process.

## 2026-05-04 - Command-Line Credential Masking in Logs

**Vulnerability:** Information Disclosure (Credentials in Logs)

**Learning:** When starting an MCP server via `StdioTransport`, the full command and arguments are logged. If these arguments contain sensitive information like API keys or tokens (e.g., `--api-key=SECRET`), they will be leaked to the system logs in plain text.

**Prevention:** Implement a masking mechanism in the transport's startup logic to identify and redact sensitive keywords (`API_KEY`, `TOKEN`, `SECRET`, etc.) and their associated values before logging the command line. This ensures that even if credentials are passed via CLI flags, they are not permanently stored in logs.
