import logging
import shutil
from typing import Dict, Any, List

try:
    from gassist_sdk.mcp import MCPClient, StdioTransport, sanitize_name
except ImportError:
    # Handle environment where SDK might not be available
    def sanitize_name(name: str) -> str:  # type: ignore[misc]
        """Fallback name sanitizer matching SDK implementation."""
        return name.replace("-", "_").replace(" ", "_")

logger = logging.getLogger(__name__)

class MCPManager:
    def __init__(self):
        self.clients: Dict[str, 'MCPClient'] = {}
        self.tool_maps: Dict[str, Dict[str, str]] = {}
        self.tools_cache: Dict[str, List[Dict[str, Any]]] = {}
        self._tool_to_client_map: Dict[str, str] = {}

    def start_clients(self, servers_config: List[Dict[str, Any]]) -> None:
        """Starts MCP clients based on configuration."""
        for s in servers_config:
            try:
                name = s.get("name")
                cmd_raw = s.get("command")
                args = s.get("args") or []
                if not cmd_raw:
                    continue

                # Security: Validate for shell metacharacters to prevent injection
                forbidden = StdioTransport.FORBIDDEN_METACHARS
                if any(any(f in str(part) for f in forbidden) for part in [cmd_raw] + args):
                    logger.error(f"[MCP] {name} initialization blocked: Potential shell injection detected.")
                    continue

                cmd = shutil.which(cmd_raw) or cmd_raw
                transport = StdioTransport(command=[cmd] + args)
                client = MCPClient(transport)

                if client.initialize():
                    self.clients[name] = client
                    try:
                        # 雙向映射：{sanitized_name: original_name}，保留原始名稱供 MCP server 呼叫
                        tools_list = client.list_tools()
                        self.tools_cache[name] = tools_list

                        client_tool_map = {}
                        for t in tools_list:
                            sanitized = sanitize_name(t["name"])
                            client_tool_map[sanitized] = t["name"]
                            # 建立反向查詢快取：若多個 server 有同名工具，採先註冊者優先 (與原本迴圈邏輯一致)
                            if sanitized not in self._tool_to_client_map:
                                self._tool_to_client_map[sanitized] = name

                        self.tool_maps[name] = client_tool_map
                    except Exception:
                        logger.error(f"[MCP] Failed to list tools for {name}", exc_info=True)
                        self.tool_maps[name] = {}
                    logger.info(f"[MCP] {name} bridge established.")
                else:
                    logger.error(f"[MCP] {name} initialization failed to return True.")

            except Exception:
                logger.error(f"[MCP] {s.get('name', 'Unknown')} initialization failed", exc_info=True)

    def call_tool(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Routes tool call to the appropriate client."""
        if tool_name in self._tool_to_client_map:
            name = self._tool_to_client_map[tool_name]
            try:
                client = self.clients[name]
                tools = self.tool_maps[name]
                # 使用 original_name（MCP server 所需），而非 sanitized 名稱
                original_name = tools[tool_name]
                res = client.call_tool(original_name, args)
                return str(res)
            except Exception:
                logger.error(f"[MCP] Error calling tool {tool_name} on client {name}", exc_info=True)
                return (
                    f"❌ MCP 工具 `{tool_name}` 執行失敗 (伺服器: `{name}`)。\n"
                    "這通常是因為工具內部發生錯誤或輸入參數格式不符。\n\n"
                    "🛠️ 解決步驟：\n"
                    f"1. 請檢查 MCP 伺服器 `{name}` 是否正常運作。\n"
                    "2. 嘗試執行「列出目前可用的工具」以確認工具狀態。\n"
                    "3. 確認輸入參數是否正確。\n"
                    "4. 查看外掛日誌以獲取詳細錯誤訊息。"
                )

        return (
            f"❌ 找不到 MCP 工具 `{tool_name}`。\n"
            "這可能是因為工具名稱拼字錯誤，或該 MCP 伺服器尚未啟動。\n\n"
            "🛠️ 解決步驟：\n"
            "1. 請確認 MCP 伺服器已正確連接且狀態為運作中。\n"
            "2. 嘗試執行「列出目前可用的工具」以確認工具名稱。\n"
            "3. 重新啟動外掛程式以重新載入工具清單。\n"
            "4. 查看日誌確認是否有 MCP 伺服器啟動失敗的紀錄。"
        )
