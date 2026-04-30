## 2025-02-27 - Text-based UI Conversational UX
**Learning:** This application uses a text-based conversational interface (G-Assist streaming) rather than a traditional visual DOM (HTML/CSS). Standard web accessibility (ARIA labels, DOM focus) does not apply. Instead, UX improvements must focus on conversational empty states, actionable error messages, and prompt suggestions.
**Action:** When working on text-based agents, prioritize adding example commands to empty states and ensuring text outputs guide the user effectively.

## 2025-02-27 - Actionable Conversational Errors
**Learning:** In a text-based, terminal-like interface, error messages that simply state the problem (e.g., "Missing SDK") are unhelpful since the user cannot click a button to resolve it. Actionable steps are critical for UX here.
**Action:** Always format error messages to include a specific, copy-pasteable command or actionable step using the "🛠️ 解決步驟：" prefix.

## 2024-05-18 - Fix Silent Failure UX in Text-based UI
**Learning:** Silent failures in text-based conversational interfaces are especially jarring because users lack visual cues like loading spinners or error toasts. It's critical to ensure synchronous validation and initialization errors from underlying components bubble up correctly to the user.
**Action:** When integrating subcomponents (e.g., intent routers) in conversational handlers, always capture and return their error states instead of defaulting to empty responses.
