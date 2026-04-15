import os
import queue
import threading
import logging
from typing import Optional, Dict, Any, TYPE_CHECKING
from vision.diagnostic import capture_diagnostic_snapshot

if TYPE_CHECKING:
    from mcp.client import MCPManager

logger = logging.getLogger(__name__)

class IntentRouter:
    def __init__(self, config: Dict[str, Any], mcp_manager: 'MCPManager', registry):
        self.config = config
        self.mcp_manager = mcp_manager
        self.registry = registry
        self._client = None

    def _init_gemini(self) -> str:
        """Initializes the Gemini client if not already initialized."""
        if self._client:
            return ""

        try:
            from google import genai

            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                key_file = os.path.join(self.registry.plugin_dir, "gemini-api.key")
                if not os.path.exists(key_file):
                    return "❌ 請設定 GEMINI_API_KEY 環境變數或檢查 gemini-api.key 設定。"
                with open(key_file, "r", encoding="utf-8") as f:
                    key = f.read().strip()

            self._client = genai.Client(api_key=key)
            return ""
        except ImportError:
            return "❌ SDK missing: google-genai is not installed."
        except Exception as e:
            return f"❌ Gemini Engine Fault: {e}"

    def process_query(self, user_query: str, plugin_stream_func) -> str:
        """Processes a query in a background thread and streams results."""
        error = self._init_gemini()
        if error:
            return error

        res_q = queue.Queue()

        def process():
            try:
                from google.genai.types import Content, Part, GenerateContentConfig, Tool, FunctionDeclaration, GoogleSearch

                func_decls = [FunctionDeclaration(name="capture_diagnostic_snapshot", description="截取當前系統畫面進視覺分析。")]
                for f in self.registry.all_functions():
                    func_decls.append(FunctionDeclaration(name=f.name, description=f.description))

                tools = [Tool(function_declarations=func_decls), Tool(google_search=GoogleSearch())]

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

                for _ in range(5):
                    resp = self._client.models.generate_content(
                        model=self.config["gemini_model"],
                        contents=contents,
                        config=GenerateContentConfig(tools=tools)
                    )

                    contents.append(Content(role="model", parts=resp.parts))
                    calls = [p.function_call for p in resp.parts if p.function_call]

                    if not calls:
                        res_q.put(("text", "".join([p.text for p in resp.parts if p.text or ""])))
                        break

                    results = []
                    for call in calls:
                        fn = call.name
                        plugin_stream_func(f"⚡ [Executing] {fn}...")

                        if fn == "capture_diagnostic_snapshot":
                            res_val = capture_diagnostic_snapshot()
                        else:
                            res_val = self.mcp_manager.call_tool(fn, dict(call.args))

                        results.append(Part.from_function_response(name=fn, response={"result": res_val}))

                    contents.append(Content(role="user", parts=results))

                res_q.put(("done", None))

            except Exception as e:
                logger.error(f"Error processing intent: {e}")
                res_q.put(("error", str(e)))

        threading.Thread(target=process, daemon=True).start()
        plugin_stream_func("💠 [Vault Analysis Initiated...]\n")

        while True:
            try:
                m, d = res_q.get(timeout=120)
                if m == "text":
                    plugin_stream_func(d)
                elif m in ("done", "error"):
                    break
            except queue.Empty:
                logger.error("Intent processing timed out.")
                break

        return ""
