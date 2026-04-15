# 📖 System Workflow Agent 用戶手冊

歡迎使用 Antigravity DevCore System Workflow Agent。
本指南將協助您快速上手如何與這名「虛擬系統工程師」互動。

## 🗣️ 如何與 Agent 互動？

您可以透過 NVIDIA Overlay (預設快捷鍵 `Alt+Z`) 喚出 G-Assist 介面，並直接輸入**繁體中文**指令。

### 常見指令範例

#### 1. 系統控制與狀態
* 「請幫我初始化系統模組」
* 「目前的系統狀態如何？」
* 「幫我執行系統視覺診斷，檢查桌面有沒有異常錯誤訊息」

#### 2. 開發者工作流 (GitKraken MCP)
* 「列出目前專案的所有 Git 分支」
* 「幫我分析最近一次的 commit 變更內容」
* 「目前的 Git 狀態為何？」

#### 3. 專業諮詢
* 「我遇到一個 Python ImportError，請幫我分析可能的原因」
* 「推薦幾個適合前端開發的 VS Code 擴充套件」

## ⚙️ 故障排除

* **Q: Agent 回覆「MCP Link Error」怎麼辦？**
  * A: 請確認您的電腦是否已安裝 Node.js，並且 `npx` 指令可以在命令提示字元中正常執行。預設的 GitKraken MCP 需要 Node.js 環境。
* **Q: Agent 提示缺少 Gemini API Key？**
  * A: 請前往外掛安裝目錄 (`C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent`)，確認 `gemini-api.key` 檔案存在且內容正確無換行。
* **Q: 無法喚出 G-Assist 或沒有反應？**
  * A: 請嘗試重新啟動 NVIDIA App，或檢查 `agent_data\system_workflow_agent.log` 檔案中的錯誤訊息。
