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

## 2026-05-04 - Sensitive Data Leakage in MCP Logs

**Vulnerability:** Information Disclosure via System Logs

**Learning:** When spawning MCP servers via `StdioTransport`, command-line arguments often contain sensitive credentials (e.g., `--api-key`). Logging the raw command line for diagnostic purposes can lead to credential leakage in log files.

**Prevention:** Implement a masking mechanism in the transport layer to redact sensitive argument values (identified by keywords like `API_KEY`, `TOKEN`, etc.) before logging the startup command.
