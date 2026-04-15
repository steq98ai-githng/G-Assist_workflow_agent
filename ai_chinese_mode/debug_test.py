# SPDX-License-Identifier: Apache-2.0
"""
Stand-alone Diagnostic & GUI for System Workflow Agent v4.0.4.2
修復 LogLevel 導入錯誤。
"""

import os
import sys
import threading
import time

# --- Setup Paths ---
_plugin_dir = os.path.dirname(os.path.abspath(__file__))
_libs_path = os.path.join(_plugin_dir, "libs")
if os.path.exists(_libs_path) and _libs_path not in sys.path:
    sys.path.insert(0, _libs_path)

print("💠 Antigravity 首席系統工程師：本機直接測試模式")
print("---------------------------------------------------")

try:
    import plugin
    # 從 SDK 內部正確路徑導入，避免 __init__.py 沒暴露的問題
    from gassist_sdk.types import LogLevel
except ImportError as e:
    print(f"❌ SDK 導入失敗: {e}")
    sys.exit(1)

# --- Check API Key ---
KEY_FILE = os.path.join(_plugin_dir, "gemini-api.key")
if not os.environ.get("GEMINI_API_KEY") and not os.path.exists(KEY_FILE):
    print("❌ 錯誤: 請設定 GEMINI_API_KEY 環境變數或建立 gemini-api.key 後再執行。")
    sys.exit(1)

print("✅ SDK & API 密鑰載入成功。")
print(f"📂 資料存放區: {plugin.DATA_DIR}")

def start_mcp():
    print("⏳ 正在啟動 GitKraken MCP 橋接...")
    try:
        plugin.init_mcp_bridge()
        time.sleep(2)
        print("✅ MCP 橋接模組已掛載。")
    except Exception as e:
        print(f"⚠️ MCP 橋接警告: {e}")

# 啟動 MCP
threading.Thread(target=start_mcp, daemon=True).start()

print("\n🤖 系統就緒。請輸入測試指令 (例如：'分析 Git 分支') 或 exit 退出:")
while True:
    try:
        user_input = input(">>> ")
        if not user_input.strip(): continue
        if user_input.lower() in ("exit", "quit"):
            break
        
        print("\n💠 [Agentic Loop 思考中...]")
        
        # 攔截 plugin.plugin.stream
        def mock_stream(data):
            print(data, end="", flush=True)
        
        old_stream = plugin.plugin.stream
        plugin.plugin.stream = mock_stream
        
        try:
            # 直接執行核心推論邏輯
            plugin.run_agentic_workflow(user_input)
        except Exception as ex:
            print(f"\n❌ 執行錯誤: {ex}")
        finally:
            plugin.plugin.stream = old_stream
            
        print("\n" + "-"*50)
    except KeyboardInterrupt:
        break

print("\n👋 測試結束。")
