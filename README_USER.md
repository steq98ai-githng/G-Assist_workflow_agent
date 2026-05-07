# 📖 System Workflow Agent 用戶手冊

歡迎使用 Antigravity DevCore System Workflow Agent。
本指南將協助您快速上手如何與這名「虛擬系統工程師」互動。

## 🗣️ 如何與 Agent 互動？

您可以透過 NVIDIA Overlay (預設快捷鍵 `Alt+Z`) 喚出 G-Assist 介面，並直接輸入**繁體中文**指令。

### 常見指令範例

#### 1. 系統控制與狀態
* 「系統效能診斷」
* 「請幫我初始化系統模組」
* 「目前的系統狀態如何？」
* 「幫我執行系統視覺診斷，檢查桌面有沒有異常錯誤訊息」
* 「列出目前可用的工具」

#### 2. 開發者工作流 (GitKraken MCP)
* 「Git 工作流優化」
* 「列出目前專案的所有 Git 分支」
* 「幫我分析最近一次的 commit 變更內容」

#### 3. 代碼自動重構分析
* 「對這段程式碼進行自動重構分析」
* 「我遇到一個 Python ImportError，請幫我分析可能的原因」
* 「分析這段程式碼並提供效能優化建議」

## ⚙️ 故障排除

* **Q: Agent 回覆「找不到 MCP 工具」或「MCP 連線錯誤」怎麼辦？**
  * A: 請確認您的電腦是否已安裝 Node.js，並且 `npx` 指令可以在命令提示字元中正常執行。預設的 GitKraken MCP 需要 Node.js 環境。
* **Q: Agent 提示缺少 Gemini API Key？**
  * A: 請前往外掛安裝目錄 (`C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent`)，確認 `gemini-api.key` 檔案存在且內容正確無換行。
* **Q: 無法喚出 G-Assist 或沒有反應？**
  * A: 請嘗試重新啟動 NVIDIA App，或檢查 `agent_data\system_workflow_agent.log` 檔案中的錯誤訊息。
