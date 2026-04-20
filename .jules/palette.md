## 2025-02-27 - Text-based UI Conversational UX
**Learning:** This application uses a text-based conversational interface (G-Assist streaming) rather than a traditional visual DOM (HTML/CSS). Standard web accessibility (ARIA labels, DOM focus) does not apply. Instead, UX improvements must focus on conversational empty states, actionable error messages, and prompt suggestions.
**Action:** When working on text-based agents, prioritize adding example commands to empty states and ensuring text outputs guide the user effectively.

## 2025-02-27 - Actionable Conversational Error Messages
**Learning:** In a text-based conversational interface without a traditional UI, terse technical error messages (e.g., "SDK missing", "Engine Fault") lead to poor UX because the user cannot "click" anywhere to fix the problem. Users need the guidance embedded directly within the text output.
**Action:** Always structure error messages with a clear problem statement followed by actionable "💡 提示" (Hints) or "🛠️ 解決步驟" (Troubleshooting steps) that tell the user exactly what command to run or where to look.
