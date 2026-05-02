import logging
import shutil
from typing import Dict, Any, List

try:
    from gassist_sdk.mcp import MCPClient, StdioTransport
except ImportError:
    # Handle environment where SDK might not be available
    pass

logger = logging.getLogger(__name__)

class MCPManager:
    def __init__(self):
        self.clients: Dict[str, 'MCPClient'] = {}
        self.tool_maps: Dict[str, Dict[str, str]] = {}

    def start_clients(self, servers_config: List[Dict[str, Any]]) -> None:
        """Starts MCP clients based on configuration."""
        for s in servers_config:
            try:
                name = s.get("name")
                cmd = shutil.which(s["command"]) or s["command"]
                args = s.get("args", [])

                transport = StdioTransport(command=[cmd] + args)
                client = MCPClient(transport)

                if client.initialize():
                    self.clients[name] = client
                    try:
                        self.tool_maps[name] = {t["name"]: t["name"] for t in client.list_tools()}
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
        for name, tools in self.tool_maps.items():
            if tool_name in tools:
                try:
                    client = self.clients[name]
                    res = client.call_tool(tool_name, args)
                    return str(res)
                except Exception:
                    logger.error(f"[MCP] Error calling tool {tool_name} on client {name}", exc_info=True)
                    return (
                        f"❌ MCP 工具 `{tool_name}` 執行失敗 (伺服器: `{name}`)。\n\n"
                        "🛠️ 解決步驟：\n"
                        f"1. 請檢查 MCP 伺服器 `{name}` 是否正常運作。\n"
                        "2. 確認輸入參數是否正確。\n"
                        "3. 查看外掛日誌以獲取詳細錯誤訊息。"
                    )

        return (
            f"❌ 找不到 MCP 工具 `{tool_name}`。\n\n"
            "🛠️ 解決步驟：\n"
            "1. 請確認 MCP 伺服器已正確連接且狀態為運作中。\n"
            "2. 嘗試重新啟動外掛程式以重新載入工具清單。\n"
            "3. 查看日誌確認是否有 MCP 伺服器啟動失敗的紀錄。"
        )
