# 💠 System Workflow Agent v4.0.4 (Mod.io / Standalone)

## 🎯 核心能力
- **Agentic MCP Bridge**: 整合 GitKraken 等 MCP 伺服器，由 Gemini AI 自動調用。
- **Developer Workflow**: 支援繁體中文代碼審查與系統效能診斷。
- **G-Assist Protocol V2**: 符合 NVIDIA 2025/2026 最新外掛規範。

## ⚙️ 安裝與測試
1. **Gemini API Key**: 請設定 `GEMINI_API_KEY` 環境變數，或將您的 API Key 填入 `gemini-api.key` (純文字檔)。
2. **啟動測試 (Standalone)**: 雙擊 `run_agent.bat`。
3. **進入 G-Assist**: 在 NVIDIA App 中對著助理下指令，例如：「幫我分析目前的 Git 分支變更」。

## 🚀 技術架構
- **Protocol**: JSON-RPC 2.0 / Length-prefixed binary framing.
- **MCP Client**: Auto-discovery with `FunctionRegistry`.
- **Persona**: Antigravity DevCore - 首席系統工程師。
