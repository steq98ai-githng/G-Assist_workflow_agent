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

## 2026-05-05 - Masking Sensitive MCP Startup Arguments

**Vulnerability:** Information Disclosure (Sensitive Data in Logs)

**Learning:** When starting MCP servers via `StdioTransport`, command-line arguments often contain sensitive credentials (API keys, tokens). Logging the full command string results in credential leakage to system logs.

**Prevention:** Implement a masking helper that redacts values associated with sensitive keywords (e.g., `API_KEY`, `TOKEN`) in both `--key=value` and `--key value` formats before logging the command execution.

## 2026-05-06 - Comprehensive Subprocess Environment Sanitization

**Vulnerability:** Information Disclosure (Credential Leakage)

**Learning:** Initializing subprocesses with a user-provided `env` dictionary can bypass default environment sanitization if the provided dictionary itself contains sensitive keys. Merging `os.environ` with the custom `env` *before* filtering is necessary to ensure no credentials leak into the child process.

**Prevention:** In `StdioTransport.__init__`, merge all environment sources first, then iterate through the resulting dictionary to remove any keys matching `SENSITIVE_KEYWORDS` before passing it to `subprocess.Popen`.
