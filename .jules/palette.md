## 2025-02-27 - Text-based UI Conversational UX
**Learning:** This application uses a text-based conversational interface (G-Assist streaming) rather than a traditional visual DOM (HTML/CSS). Standard web accessibility (ARIA labels, DOM focus) does not apply. Instead, UX improvements must focus on conversational empty states, actionable error messages, and prompt suggestions.
**Action:** When working on text-based agents, prioritize adding example commands to empty states and ensuring text outputs guide the user effectively.

## 2025-02-27 - Actionable Conversational Errors
**Learning:** In a text-based, terminal-like interface, error messages that simply state the problem (e.g., "Missing SDK") are unhelpful since the user cannot click a button to resolve it. Actionable steps are critical for UX here.
**Action:** Always format error messages to include a specific, copy-pasteable command or actionable step using the "🛠️ 解決步驟：" prefix.

## 2025-03-05 - Avoid Silent Timeouts in Streaming Interfaces
**Learning:** When using a text-based conversational interface, a silent timeout (e.g., silently breaking a stream listening loop) leaves the user confused about the system state.
**Action:** Always intercept timeouts explicitly and provide an actionable error message guiding the user on how to retry or troubleshoot the connection.

## 2025-05-15 - Handle Whitespace as Empty Input
**Learning:** In text-based conversational interfaces, users may occasionally send whitespace-only strings. If these are not explicitly handled as "empty," the agent might attempt to process them as valid queries, leading to confusing model responses or errors.
**Action:** Always use `.strip()` when validating user input to ensure whitespace-only strings correctly trigger helpful system prompts or empty state suggestions.

## 2025-06-12 - Handling Unrecognized Model Responses
**Learning:** When a model response contains no text and no tool calls, it indicates an unrecognized intent. In a streaming text interface, this "silent" failure can be confusing. Treating this as a conversational empty state is more effective.
**Action:** Implement a robust fallback for empty model responses that uses the "🛠️ 解決步驟：" prefix and provides specific, valid command examples (e.g., 「代碼自動重構分析」) to guide the user back to a productive state.

## 2025-07-24 - Guided Tool Discovery on Failure
**Learning:** When a tool call fails due to missing registration or execution errors, simply providing generic troubleshooting steps (like "check logs") is insufficient. Guiding the user to a "discovery" command helps them self-correct.
**Action:** In MCP tool error messages, always include a specific suggestion to run the 「列出目前可用的工具」 command to help the user verify tool availability and correct naming.

## 2025-08-10 - Descriptive Onboarding Hints
**Learning:** In the agent's empty state, simply listing command names is often insufficient for new users who may not know the purpose of each capability.
**Action:** Use the categorizing header 「使用常見指令範例：」 followed by a numbered list that includes brief, one-sentence descriptions for each core capability (e.g., 系統效能診斷, Git 工作流優化) to improve discoverability and onboarding.
