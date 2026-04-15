# 💠 System Workflow Agent v4.0.4 (AI 中文版)

> 專為 **NVIDIA Project G-Assist** 打造的「中文大腦」與「系統工程師代理」。
> 讓 G-Assist 完全聽懂中文，並整合 Gemini AI 語意理解、電腦視覺診斷以及 Agentic MCP 工作流（支援 GitKraken 等工具）。

![G-Assist](https://img.shields.io/badge/Project-G--Assist-76B900?logo=nvidia)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/Version-v4.0.4-orange)
![Protocol](https://img.shields.io/badge/Protocol-V2-brightgreen)

## 🎯 這是什麼？

System Workflow Agent (又稱 AI 中文版) 是一款符合 NVIDIA 2025/2026 最新外掛規範 (Protocol V2) 的 G-Assist Plugin。
它將原本以遊戲輔助為主的 G-Assist，升級為具備「首席系統工程師」職責的生產力工具，讓您可以直接用流利的**繁體中文**命令您的 RTX PC。

## ✨ 核心能力與特色

| 功能模塊 | 說明 | 依賴 |
| :--- | :--- | :--- |
| 🇹🇼 **中文原生意圖** | 直接接收並理解中文指令（如「初始化」、「關閉」、「系統狀態」），完美映射到內部生命週期或控制功能。 | ❌ |
| 🧠 **Gemini AI 擴充** | 整合 Google Gemini 2.0 模型作為大腦，提供專業的「Antigravity DevCore」首席工程師 Persona。 | ✅ 需 Gemini Key |
| 🔌 **Agentic MCP Bridge** | 內建 MCP (Model Context Protocol) Client，自動發現並動態註冊工具，預設支援 **GitKraken** 等 MCP Server，實現 AI 自動代碼審查與版本控制分析。 | ❌ (內建) |
| 👁️ **Vision 系統診斷** | 具備視覺多模態能力 (`vision_diagnostic`)，可截取系統畫面並交由 AI 分析效能面板或錯誤訊息。 | ✅ 需 Gemini Key |
| ⚡ **Protocol V2 加固** | 移除過時的 Heartbeat loop，採用 V2 原生的 `FunctionRegistry` 與 JSON-RPC 2.0 穩定通訊，確保高負載下不阻塞。 | ❌ |

## 🚀 快速安裝與啟動

### 前置準備
- 已安裝 NVIDIA App 與 Project G-Assist。
- Python 3.x 環境。
- Node.js (如需使用預設的 npx 啟動 GitKraken MCP)。

### 安裝步驟

1. **進入專案目錄**
   ```bash
   cd ai_chinese_mode
   ```

2. **執行安裝腳本**
   雙擊執行 `install.bat`。
   > ⚠️ **注意**：腳本會自動請求管理員權限，以將外掛複製到 G-Assist 的核心目錄 (`C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent`)。請在跳出的 UAC 視窗點選「是」。

3. **重新啟動服務**
   重新啟動 **NVIDIA App** 與 **Project G-Assist**。

## 💡 使用方式

安裝後，您可以透過 NVIDIA Overlay（Alt+Z）直接用中文對話，或者在桌面直接呼叫 G-Assist。

### 常用中文指令範例
- **系統控制：**「請幫我初始化系統」、「系統狀態如何？」、「關閉服務」
- **開發者工作流 (需設定 MCP/Gemini)：**「幫我分析目前的 Git 分支變更」、「執行系統視覺分析，看看效能面板數據有沒有異常」
- **一般 AI 問答：**「幫我推薦幾個 VS Code 擴充套件」

## ⚙️ 進階設定 (Gemini & MCP)

### 設定檔位置
外掛安裝後，資料與設定會存放在：
`C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent\`

您可以在此目錄中找到：
- `config.json`: 設定使用的 Gemini 模型版本與 MCP Server 指令。
- `gemini-api.key`: 請建立此純文字檔，並將您的 [Gemini API Key](https://aistudio.google.com/app/apikey) 貼入其中（單行字串）。

### config.json 範例
```json
{
  "gemini_model": "gemini-2.0-flash",
  "mcp_servers": [
    {
      "name": "GitKraken",
      "command": "npx",
      "args": ["-y", "@gitkraken/mcp-server"]
    }
  ]
}
```

## 📂 專案結構

```
.
├── README.md               # 專案總覽說明 (本文件)
├── AIChineseControlSkill   # 獨立的 IDE/Agent 測試版程式碼 (無依賴)
└── ai_chinese_mode/        # G-Assist 外掛主目錄
    ├── plugin.py           # 核心外掛程式碼 (v4.0.4)
    ├── manifest.json       # G-Assist V2 規範設定檔
    ├── test_plugin.py      # 自動化單元測試腳本
    ├── install.bat         # Windows 一鍵安裝腳本
    ├── run_agent.bat       # 獨立測試啟動腳本
    ├── package_v4.py       # 打包腳本
    ├── README_USER.md      # 使用者手冊舊檔參考
    ├── README_MODIO.md     # Mod.io 發布說明
    └── libs/
        └── gassist_sdk/    # G-Assist SDK Protocol V2 模組
```

## 🧪 自動化測試

本專案包含單元測試，以確保 V4 Manifest 純淨度與 MCP 設定：

```bash
cd ai_chinese_mode
python -m unittest test_plugin.py
```

## 🤝 貢獻與開發

歡迎提交 PR 擴充此中文大腦！請遵循 [NVIDIA G-Assist 貢獻指南](https://github.com/NVIDIA/G-Assist/blob/main/CONTRIBUTING.md)。

## 📄 授權條款

本專案採用 **MIT License** 授權。
有關外掛模板及 SDK 內容，歸 NVIDIA 及其 Apache License 2.0 授權所有。
