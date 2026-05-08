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

## 2026-05-05 - Sensitive Data in Subprocess Logs

**Vulnerability:** Information Disclosure via System Logs

**Learning:** When spawning subprocesses with command-line arguments, sensitive information such as API keys or tokens may be passed as arguments. Logging the raw command line can leak these secrets into system logs or developer consoles.

**Prevention:** Implement a masking helper that redacts values associated with sensitive keywords (e.g., `API_KEY`, `TOKEN`) in both `--key=value` and `--key value` formats before logging the command execution.

## 2026-05-07 - Sensitive Data in Intent Handler Logs

**Vulnerability:** Information Disclosure (Sensitive Data in Logs)

**Learning:** Logging raw user input at the `INFO` level in intent handlers (e.g., `GitIntentHandler`, `SystemIntentHandler`) can leak sensitive information (passwords, tokens, private data) into system logs, which may be accessible to unauthorized users or stored insecurely.

**Prevention:** Restrict logging of raw user input to `DEBUG` or `TRACE` levels. For `INFO` level logs, only record metadata such as the length of the input to provide operational visibility without compromising security.

## 2026-05-08 - Subprocess Logging and Injection Hardening

**Vulnerability:** Information Disclosure and Subprocess Injection Risk

**Learning:** The `_mask_sensitive_args` logic was incorrectly masking the *next* argument for any sensitive keyword, which could leak the sensitive value itself if it wasn't a flag, and mask a safe argument instead. Additionally, shell metacharacter validation was missing the space character, which could be used in some environments to bypass certain shell-like parsing checks.

**Prevention:** Ensure `_mask_sensitive_args` only triggers "mask next" behavior for actual flags (starting with `-`). Standalone sensitive values must be masked immediately. Add the space character to `FORBIDDEN_METACHARS` to further restrict command string interpretation.
