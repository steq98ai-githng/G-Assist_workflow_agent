# G-Assist 中文外掛 v2.0 (AI Chinese Mode)

> 讓 NVIDIA G-Assist 完全聽懂中文，整合 Gemini AI 語意理解、即時天氣、Discord 訊息發送。

## 功能總覽

| 功能 | 說明 | 需要 API Key |
|------|------|:---:|
| 🇹🇼 中文指令 | 15+ 中文關鍵字映射到 G-Assist 原生功能 | ❌ |
| 🌤️ 天氣查詢 | Open-Meteo API，支援 20+ 中文城市名 | ❌ |
| 📨 Discord | Webhook 模式發送訊息到頻道 | 需 Webhook URL |
| 🤖 Gemini AI | 關鍵字未匹配時自動 Fallback 到 Gemini | 需 Gemini Key |
| 🔄 持續對話 | 啟動後保持中文對話模式 | ❌ |

## 快速安裝

### 方法一：直接複製
```bash
# 複製外掛到 G-Assist plugins 目錄
xcopy /E /I "ai_chinese_mode" "%PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins\ai_chinese_mode"
```

### 方法二：使用 install.bat
```bash
install.bat
```

## 使用方式

安裝後，透過 NVIDIA Overlay（Alt+Z）直接用中文對話：

### 系統控制
- 「初始化」/ 「啟動」/ 「開始」
- 「關閉」/ 「停止」/ 「結束」
- 「重啟」/ 「重新啟動」
- 「系統狀態」

### 遊戲功能
- 「顯示FPS」/ 「關閉FPS」
- 「最佳化」
- 「截圖」/ 「錄影」/ 「停止錄影」
- 「溫度」/ 「GPU溫度」/ 「顯卡溫度」

### 天氣查詢（免 API Key）
- 「台北天氣」
- 「東京的天氣如何」
- 「高雄天氣」

### Discord 發送
- 「發到Discord 大家好！」
- 「傳到Discord 我正在玩遊戲」

### AI 智慧問答（需 Gemini Key）
- 直接問任何問題，例如：「2025 年最好的顯卡是什麼？」
- 關鍵字未匹配時自動啟用 Gemini AI

## 設定

### 設定檔位置
```
%PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins\ai_chinese_mode\config.json
```

### 設定項目
```json
{
  "gemini_model": "gemini-2.5-flash",
  "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN",
  "weather_default_city": "台北",
  "language": "zh-TW"
}
```

### Gemini API Key
1. 前往 https://aistudio.google.com/app/apikey
2. 建立 API Key
3. 設定為 `GEMINI_API_KEY` 環境變數，或存入：`%PROGRAMDATA%\...\ai_chinese_mode\gemini-api.key`
4. 或在對話中直接貼上 Key，外掛會自動儲存

### Discord Webhook
1. 在 Discord 頻道設定 → 整合 → Webhook
2. 建立新 Webhook，複製 URL
3. 貼入 `config.json` 的 `discord_webhook_url`

## 專案結構

```
ai_chinese_mode/
├── plugin.py          # 主程式（v2.0 整合版）
├── manifest.json      # G-Assist 外掛配置（4 功能路由）
├── config.json        # 使用者設定（自動建立）
├── requirements.txt   # Python 依賴
├── test_plugin.py     # 自動化測試（52 個斷言）
├── install.bat        # 安裝腳本
├── libs/
│   └── gassist_sdk/   # G-Assist SDK v3.1.0
└── README_USER.md     # 本文件
```

## 技術架構

```
使用者 (中文語音/文字)
        │
        ▼
  ┌─────────────┐
  │ 意圖偵測引擎 │ ← 15+ 中文關鍵字映射
  │ (keyword)    │
  └──────┬──────┘
         │
    ┌────┴────┐
    │ 有匹配？ │
    ├─ Yes ───→ 直接執行對應功能回應
    │         ├── 天氣 → Open-Meteo API
    │         ├── Discord → Webhook POST
    │         └── 其他 → 中文回應字典
    │
    └─ No ────→ Gemini AI Fallback
               ├── 有 Key → 串流回應
               └── 無 Key → 提示設定
```

## 測試

```bash
python test_plugin.py
```

預期輸出：`📊 測試結果：52/52 通過 🎉`

## 授權

Apache License 2.0

## 貢獻

歡迎提交 PR！請遵循 [NVIDIA G-Assist 貢獻指南](https://github.com/NVIDIA/G-Assist/blob/main/CONTRIBUTING.md)。
