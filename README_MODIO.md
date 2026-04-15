# 🇹🇼 G-Assist 中文外掛 (AI Chinese Mode) 

**版本:** v3.0.0 | **支援 G-Assist Protocol V2**

讓 NVIDIA G-Assist 完全聽懂中文！不只是簡單的對話，這是一款結合了 **Gemini AI 推論能力** 與 **MCP (Model Context Protocol) 無限工具擴充** 的「Agentic（代理型）」外掛。

💬 支援：繁體中文、簡體中文的文字與語音輸入

## ✨ 核心特色功能

1. **原生指令中文化 mapping**  
   直接用中文說出：「顯示 FPS」、「幫我最佳化遊戲」、「系統目前的狀態」、「截圖」、「錄影」，系統將自動無縫呼叫 G-Assist 本機原生指令。

2. **即時天氣與實用小工具 (免 API Key)**  
   說出「台北天氣」、「今天下雨嗎」，透過 Open-Meteo 自動精準查詢並回報中文。

3. **Discord 遊戲語音連動**  
   激戰中不想切換畫面？說出「傳到 Discord 大家好」，即可直接將語音轉為文字，發送至您指定的伺服器頻道。

4. **🚀 Agentic MCP 代理控制 (核心創新)**  
   此模組自動結合 `G-Assist` 與 Google `Gemini 2.5` 模型。
   如果您配置了任何開源 MCP Server（例如：**mcp-server-filesystem**, **mcp-server-sqlite**），本外掛將自動提取所有的 Tools 並配置給 Gemini。
   當您說：「讀取我的系統日誌看看有什麼異常」，Gemini 將在背景**自動呼叫 MCP 工具**進行操作，並將分析結果用流利的中文反饋給您！

## 📦 安裝說明

1. 下載並解壓縮本 ZIP 壓縮檔。
2. 將解壓縮後的整個資料夾，放入您的 NVIDIA 插件目錄：
   `%PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins\`
3. 確保資料夾名稱為 `ai_chinese_mode`，且裡面包含 `plugin.py`。
4. 重新啟動 G-Assist (NVIDIA App)。

## ⚙️ 首次啟動與使用

- 啟動時外掛會在同目錄下自動產生 `config.json`，您可以修改裡面的：
  - `discord_webhook_url` (綁定您的 Discord Webhook)
  - `mcp_server_command` & `args` (綁定如 `npx @modelcontextprotocol/server-filesystem C:\`)
- **啟動 AI 模式**：至 Google AI Studio 申請免費的 Gemini API Key，並在對話中直接貼上或寫入 `gemini-api.key` 檔中即可啟動神經網路引擎。

## 💡 為什麼選擇這個外掛？

這不僅是個「語言翻譯包」，而是完全利用了 G-Assist SDK 的底層特性。我們建立了一個強大的 `MCPBridge`，將 G-Assist 作為您個人電腦的最終極系統介面，而 Gemini 則是為您操作 MCP 工具的代工工程師。這是釋放 RTX AI 運算力的最佳社群示範！

👉 *如果您覺得這項功能很酷，請在 mod.io 給我們一個讚與好評！*
