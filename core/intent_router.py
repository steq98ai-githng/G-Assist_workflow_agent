import os
import queue
import threading
import logging
from typing import Optional, Dict, Any, TYPE_CHECKING
from vision.diagnostic import capture_diagnostic_snapshot

if TYPE_CHECKING:
    from mcp.client import MCPManager

logger = logging.getLogger(__name__)

MAX_QUERY_LENGTH = 100_000  # 1% of 10MB MAX_MESSAGE_SIZE (aligned with v4.0.4)

class IntentRouter:
    # Maximum length for user queries to prevent resource exhaustion (1% of MAX_MESSAGE_SIZE)
    MAX_QUERY_LENGTH = MAX_QUERY_LENGTH

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
                    return (
                        "❌ 缺少 Gemini API Key。\n\n"
                        "🛠️ 解決步驟：\n"
                        "1. 在外掛目錄建立 `gemini-api.key` 檔案。\n"
                        "2. 將您的 API Key 貼入該檔案。\n"
                        "3. 或者，您也可以設定 `GEMINI_API_KEY` 環境變數。"
                    )
                with open(key_file, "r", encoding="utf-8") as f:
                    key = f.read().strip()

            self._client = genai.Client(api_key=key)
            return ""
        except ImportError:
            return (
                "❌ 缺少 google-genai SDK 套件。\n\n"
                "🛠️ 解決步驟：\n"
                "1. 請開啟命令提示字元 (CMD) 或終端機。\n"
                "2. 執行指令：`pip install google-genai`。\n"
                "3. 重新啟動外掛程式。"
            )
        except Exception:
            logger.exception("Gemini Engine initialization fault")
            return (
                "❌ Gemini 引擎初始化失敗。\n\n"
                "🛠️ 解決步驟：\n"
                "1. 請確認您的網路連線是否正常。\n"
                "2. 檢查 Gemini API Key 是否有效或已超過額度。\n"
                "3. 查看系統日誌 (log) 以獲取更多錯誤細節。"
            )

    def process_query(self, user_query: str, plugin_stream_func) -> str:
        """Processes a query in a background thread and streams results."""
        if len(user_query) > self.MAX_QUERY_LENGTH:
            return (
                f"❌ 查詢內容過長 (上限 {MAX_QUERY_LENGTH:,} 字元)。\n\n"
                "🛠️ 解決步驟：\n"
                "1. 請簡化您的查詢，或拆分成更小的任務。\n"
                "2. 避免在單一查詢中貼上大量代碼或日誌。"
            )

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
                    Content(role="user", parts=[Part.from_text(user_query)])
                ]

                for _ in range(5):
                    resp = self._client.models.generate_content(
                        model=self.config["gemini_model"],
                        contents=contents,
                        config=GenerateContentConfig(
                            tools=tools,
                            system_instruction=system_prompt,
                        )
                    )

                    contents.append(Content(role="model", parts=resp.parts))
                    calls = [p.function_call for p in resp.parts if p.function_call]

                    if not calls:
                        text_resp = "".join(p.text for p in resp.parts if p.text).strip()
                        if not text_resp:
                            text_resp = (
                                "抱歉，我無法理解您的指令或未獲得有效回應。\n\n"
                                "🛠️ 解決步驟：\n"
                                "1. 請嘗試更明確地描述您的需求。\n"
                                "2. 嘗試使用常見指令（例如：「列出目前可用的工具」、「代碼自動重構分析」）。\n"
                                "3. 檢查您的網路連線是否正常。"
                            )
                        res_q.put(("text", text_resp))
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
                plugin_stream_func(
                    "\n⏳ 處理逾時。\n\n"
                    "🛠️ 解決步驟：\n"
                    "1. 請稍後再試，可能是模型回應時間較長。\n"
                    "2. 嘗試簡化您的查詢，或拆分成更小的任務。\n"
                    "3. 檢查網路連線狀態。\n"
                    "4. 若問題持續發生，請嘗試重新啟動外掛程式。"
                )
                break

        return ""
