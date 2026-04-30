# 💠 System Workflow Agent v4.1.0
This document describes the high-level architecture of the **System Workflow Agent** v4.1.0, a specialized plugin for NVIDIA Project G-Assist.


> 專為 **NVIDIA Project G-Assist** 打造的「中文大腦」與「系統工程師代理」。
> 讓 G-Assist 完全聽懂中文，並整合 Gemini AI 語意理解、電腦視覺診斷以及 Agentic MCP 工作流（支援 GitKraken 等工具）。

![G-Assist](https://img.shields.io/badge/Project-G--Assist-76B900?logo=nvidia)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/Version-v4.1.0-orange)
![Protocol](https://img.shields.io/badge/Protocol-V2-brightgreen)

## 🎯 這是什麼？

System Workflow Agent 是一款符合 NVIDIA 2025/2026 最新外掛規範 (Protocol V2) 的 G-Assist Plugin。
它將原本以遊戲輔助為主的 G-Assist，升級為具備「首席系統工程師」職責的生產力工具，讓您可以直接用流利的**繁體中文**命令您的 RTX PC。

## 🏗️ 架構概覽

本專案採用高度模組化的設計，以確保在 G-Assist 高頻率呼叫下的穩定性。

```text
G-Assist System Workflow Agent Architecture

   [NVIDIA G-Assist App]
           │
           ▼ (Protocol V2 / JSON-RPC)
    ┌─────────────┐
    │ plugin.py   │ ─── 進入點 (Entry Point)
    └─────────────┘
           │
           ▼
  [ core/plugin_runtime.py ] ── 生命週期管理與無狀態核心
           │
           ├──► [ config/loader.py ] ── 設定檔載入與驗證
           │
           ├──► [ core/intent_router.py ] ── Gemini 2.0 推理與指令分發
           │        │
           │        ├──► [ vision/diagnostic.py ] ── 多模態視覺診斷
           │        │
           │        └──► [ mcp/client.py & mcp/registry.py ] ── 動態工具整合
           │
           └──► [ core/event_bus.py ] ── 解耦合內部事件匯流排
```

> 🔍 欲了解更多詳細技術細節，請參閱 [ARCHITECTURE.md](./ARCHITECTURE.md)。

## ✨ 核心能力與特色

| 功能模塊 | 說明 | 依賴 |
| :--- | :--- | :--- |
| 🇹🇼 **中文原生意圖** | 直接接收並理解中文指令（如「初始化」、「關閉」、「系統狀態」），完美映射到內部生命週期或控制功能。 | ❌ |
| 🧠 **Gemini AI 擴充** | 整合 Google Gemini 2.0 模型作為大腦，提供專業的「Antigravity DevCore」首席工程師 Persona。 | ✅ 需 Gemini Key |
| 🔌 **Agentic MCP Bridge** | 內建 MCP Client，自動發現並動態註冊工具，預設支援 **GitKraken** 等 MCP Server。 | ❌ (內建) |
| 👁️ **Vision 系統診斷** | 具備視覺多模態能力 (`vision_diagnostic`)，可截取系統畫面並交由 AI 分析效能面板或錯誤訊息。 | ✅ 需 Gemini Key |
| ⚡ **模組化穩定核心** | 分層架構 (`/core`, `/mcp`, `/vision`, `/config`)，確保高負載下穩定不阻塞。 | ❌ |

## 🚀 快速安裝與啟動

### 前置準備
- 已安裝 NVIDIA App 與 Project G-Assist。
- Python 3.10+ 環境。
- Node.js (如需使用預設的 npx 啟動 GitKraken MCP)。

### 安裝步驟

1. **進入專案目錄**
   確保您位於專案的根目錄。

2. **執行安裝腳本**
   雙擊執行 `install.bat`。
   > ⚠️ **注意**：腳本會自動請求管理員權限，以將外掛複製到 G-Assist 的核心目錄 (`C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent`)。

3. **設定 API Key**
   前往安裝目錄，建立 `gemini-api.key` 檔案並填入您的 Gemini API 密鑰。

4. **重新啟動服務**
   重新啟動 **NVIDIA App** 與 **Project G-Assist**。

## 🧪 自動化測試

本專案採用 `pytest` 進行單元測試：

```bash
pip install pytest
pytest tests/
```

## 📄 授權條款

本專案採用 **Apache License 2.0** 授權。
