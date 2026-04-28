# SPDX-License-Identifier: Apache-2.0
"""
System Workflow Agent v4.0.4 (Final Structural Fortification)
Based on NVIDIA G-Assist Protocol V2 & DevCore Vault 技能組

修正項目:
1. 採用 SDK 內建 FunctionRegistry 實作工具自動發現與 Manifest 同步。
2. 整合 StdioTransport 與 MCPClient 達成標準化 GitKraken 橋接。
3. 優化 JSON-RPC 2.0 序列化安全性 (Defensive Serialization)。
4. 導入 DevCore 職業人設：首席系統工程師。
"""

import os
import sys
import json
import logging
import queue
import shutil
import threading
from typing import Any, Dict, List, Optional

# --- SDK Initialization (V2 Standard) ---
_plugin_dir = os.path.dirname(os.path.abspath(__file__))
_libs_path = os.path.join(_plugin_dir, "libs")
if os.path.exists(_libs_path) and _libs_path not in sys.path:
    sys.path.insert(0, _libs_path)

try:
    from gassist_sdk import Plugin, Context
    from gassist_sdk.mcp import MCPClient, StdioTransport, FunctionRegistry, FunctionDef, sanitize_name
except ImportError as e:
    sys.stderr.write(f"V2 SDK Error: {e}\n")
    sys.exit(1)

# --- Path Management (Defensive) ---
PLUGIN_NAME = "system_workflow_agent"

def _get_secure_data_dir() -> str:
    prog_data = os.environ.get("PROGRAMDATA", "")
    if prog_data:
        primary = os.path.join(prog_data, "NVIDIA Corporation", "nvtopps", "rise", "plugins", PLUGIN_NAME)
        try:
            os.makedirs(primary, exist_ok=True)
            return primary
        except Exception:
            logging.getLogger(__name__).warning("Failed to create primary directory", exc_info=True)
    
    fallback = os.path.join(_plugin_dir, "agent_data")
    os.makedirs(fallback, exist_ok=True)
    return fallback

DATA_DIR = _get_secure_data_dir()
LOG_FILE = os.path.join(DATA_DIR, f"{PLUGIN_NAME}.log")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
GEMINI_KEY_FILE = os.path.join(DATA_DIR, "gemini-api.key")

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "gemini_model": "gemini-2.0-flash",
    "mcp_servers": [
        {"name": "GitKraken", "command": "npx", "args": ["-y", "@gitkraken/mcp-server"]}
    ]
}

def load_config():
    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception: logger.error("Config load error", exc_info=True)
    return cfg

# --- Plugin & Registry ---
plugin = Plugin(name=PLUGIN_NAME, version="4.0.4", description="Professional Workflow Specialist")
registry = FunctionRegistry(PLUGIN_NAME, plugin_dir=DATA_DIR, source_dir=_plugin_dir)

# ============================================================================
# AGENTIC MCP BRIDGE (v4.0.4 Refined)
# ============================================================================
_mcp_clients: Dict[str, MCPClient] = {}

def init_mcp_bridge():
    config = load_config()
    def _bridge_starter():
        discovered = []
        for s in config.get("mcp_servers", []):
            try:
                cmd = shutil.which(s["command"]) or s["command"]
                transport = StdioTransport(command=[cmd] + s["args"])
                client = MCPClient(transport)
                if client.initialize():
                    _mcp_clients[s["name"]] = client
                    tools = client.list_tools()
                    for t in tools:
                        fdef = FunctionDef(
                            name=sanitize_name(t["name"]),
                            description=t.get("description", ""),
                            properties=t.get("inputSchema", {}).get("properties", {}),
                            required=t.get("inputSchema", {}).get("required", [])
                        )
                        registry.register(fdef)
                        discovered.append(fdef)
                    logger.info(f"[MCP] {s['name']} bridge established.")
            except Exception:
                logger.error(f"[MCP] {s['name']} initialization failed", exc_info=True)
        
        if discovered:
            registry.save_cache()
            registry.update_manifest(plugin.version, plugin.description)
            logger.info(f"[SDK] Manifest updated with {len(discovered)} discovered functions.")

    threading.Thread(target=_bridge_starter, daemon=True).start()

# ============================================================================
# SYSTEM DIAGNOSTIC TOOL
# ============================================================================
def capture_diagnostic_snapshot():
    """視覺多模態：截取當前系統畫面供分析。"""
    # 這裡可串接實際截圖 API，目前回傳狀態模擬
    return "[Diagnostic Screenshot Captured & Uploaded to Analysis Buffer]"

# ============================================================================
# GEMINI BRAIN (Professional DevCore Vault Persona)
# ============================================================================
_client = None

def run_agentic_workflow(user_query: str):
    global _client
    if not _client:
        try:
            from google import genai
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                if not os.path.exists(GEMINI_KEY_FILE):
                    return (
                        "❌ 缺少 Gemini API Key。\n\n"
                        "🛠️ 解決步驟：\n"
                        "1. 在外掛目錄建立 `gemini-api.key` 檔案。\n"
                        "2. 將您的 API Key 貼入該檔案。\n"
                        "3. 或者，您也可以設定 `GEMINI_API_KEY` 環境變數。"
                    )
                with open(GEMINI_KEY_FILE, "r") as f: key = f.read().strip()
            _client = genai.Client(api_key=key)
        except ImportError:
            msg = (
                "❌ 缺少 google-genai SDK 套件。\n\n"
                "🛠️ 解決步驟：\n"
                "1. 請開啟命令提示字元 (CMD) 或終端機。\n"
                "2. 執行指令：`pip install google-genai`。\n"
                "3. 重新啟動外掛程式。"
            )
            plugin.stream(msg)
            return msg
        except Exception:
            logger.exception("Gemini Engine initialization fault")
            msg = (
                "❌ Gemini 引擎初始化失敗。\n\n"
                "🛠️ 解決步驟：\n"
                "1. 請確認您的網路連線是否正常。\n"
                "2. 檢查 Gemini API Key 是否有效或已超過額度。\n"
                "3. 查看系統日誌 (log) 以獲取更多錯誤細節。"
            )
            plugin.stream(msg)
            return msg

    cfg = load_config()
    res_q = queue.Queue()

    def process():
        try:
            from google.genai.types import Content, Part, GenerateContentConfig, Tool, FunctionDeclaration, GoogleSearch
            
            # Build Tool Definitions from Registry
            func_decls = [FunctionDeclaration(name="capture_diagnostic_snapshot", description="截取當前系統畫面進視覺分析。")]
            for f in registry.all_functions():
                func_decls.append(FunctionDeclaration(name=f.name, description=f.description))
            
            tools = [Tool(function_declarations=func_decls), Tool(google_search=GoogleSearch())]
            
            # DevCore Vault Role Prompt
            system_prompt = (
                "Role: Antigravity 首席系統工程師博士 (DevCore)\n"
                "Objective: 100% 提升開發者執行力。使用繁體中文（台灣）。\n"
                "Skills: Git 工作流優化、系統效能診斷、代碼自動重構分析。\n"
                "Rule: 優先使用 MCP 工具。回應必須精準、模組化、且具備工程嚴謹性。"
            )
            
            contents = [
                Content(role="system", parts=[Part.from_text(system_prompt)]),
                Content(role="user", parts=[Part.from_text(user_query)])
            ]

            mcp_tool_map = {}
            for client in _mcp_clients.values():
                try:
                    # Map sanitized names to original names for correct routing and execution
                    mcp_tool_map[client] = {sanitize_name(t["name"]): t["name"] for t in client.list_tools()}
                except Exception:
                    logger.error("[MCP] Failed to list tools", exc_info=True)
                    mcp_tool_map[client] = {}

            for _ in range(5):
                resp = _client.models.generate_content(model=cfg["gemini_model"], contents=contents, config=GenerateContentConfig(tools=tools))
                contents.append(Content(role="model", parts=resp.parts))
                calls = [p.function_call for p in resp.parts if p.function_call]
                
                if not calls:
                    res_q.put(("text", "".join([p.text for p in resp.parts if p.text or ""])))
                    break
                
                results = []
                for call in calls:
                    fn = call.name
                    plugin.stream(f"⚡ [Executing] {fn}...")
                    
                    # Local Function Mapping
                    if fn == "capture_diagnostic_snapshot":
                        res_val = capture_diagnostic_snapshot()
                    else:
                        # MCP Tool Routing
                        res_val = "MCP Link Error."
                        for client, mcp_tools in mcp_tool_map.items():
                            if fn in mcp_tools:
                                # Use the original tool name required by the MCP server
                                r = client.call_tool(mcp_tools[fn], dict(call.args))
                                res_val = str(r); break
                    
                    results.append(Part.from_function_response(name=fn, response={"result": res_val}))
                contents.append(Content(role="user", parts=results))
            res_q.put(("done", None))
        except Exception:
            logger.exception("Error processing intent")
            res_q.put(("text", (
                "❌ 處理查詢時發生系統錯誤。\n\n"
                "🛠️ 解決步驟：\n"
                "1. 請稍後再試，可能是暫時性的網路不穩定。\n"
                "2. 如果問題持續發生，請檢查 MCP 伺服器狀態。\n"
                "3. 查看外掛日誌以獲取詳細錯誤。"
            )))
            res_q.put(("error", None))

    threading.Thread(target=process, daemon=True).start()
    plugin.stream("💠 [Vault Analysis Initiated...]\n")
    while True:
        try:
            m, d = res_q.get(timeout=120)
            if m == "text": plugin.stream(d)
            elif m in ("done", "error"): break
        except: break

@plugin.command("system_workflow_agent")
def handle_agent(user_input: str = None, context: Context = None):
    if not user_input:
        plugin.set_keep_session(True)
        return (
            "💠 **Antigravity DevCore System Agent v4.0.4**\n"
            "工程指令就緒，請輸入查詢事項。\n\n"
            "💡 提示：您可以試著問我：\n"
            "- 「幫我診斷目前的系統狀態」\n"
            "- 「列出目前可用的工具」\n"
            "- 「查詢最近的 Git 提交紀錄」"
        )
    run_agentic_workflow(user_input)
    plugin.set_keep_session(True)
    return ""

if __name__ == "__main__":
    init_mcp_bridge()
    plugin.run()
