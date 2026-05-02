## 2025-05-14 - License Transition to Apache 2.0

**Vulnerability:** N/A (Compliance/Legal update)

**Learning:** When transitioning licenses, it is critical to search for all occurrences of the old license in documentation, manifests, and source code headers (SPDX identifiers).

**Prevention:** Use automated scripts to verify license headers across the repository.

## 2026-05-01 - Missing Input Length Validation

**Vulnerability:** User queries were passed to Gemini without length validation, potentially leading to resource exhaustion (DOS) or excessive API costs if extremely large inputs were provided.

**Learning:** In text-based agentic workflows, always enforce a strict upper bound on user input length at the earliest possible entry point to protect downstream services (like LLMs) and system memory.

**Prevention:** Implement a `MAX_QUERY_LENGTH` constant (e.g., 10,000 characters) and validate user input against it before initiating any processing or background threads.
