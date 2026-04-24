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
                    logger.info(f"[MCP] {name} bridge established.")
                else:
                    logger.error(f"[MCP] {name} initialization failed to return True.")

            except Exception:
                logger.error(f"[MCP] {s.get('name', 'Unknown')} initialization failed", exc_info=True)

    def call_tool(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Routes tool call to the appropriate client."""
        for client in self.clients.values():
            try:
                tools = client.list_tools()
                for t in tools:
                    if t["name"] == tool_name:
                        res = client.call_tool(tool_name, args)
                        return str(res)
            except Exception:
                logger.error(f"[MCP] Error calling tool {tool_name}", exc_info=True)

        return f"MCP Tool {tool_name} not found or execution failed."
