import logging
from typing import List

try:
    from gassist_sdk.mcp import FunctionDef, sanitize_name
except ImportError:
    # Basic mock for testing environments where SDK might be missing
    class FunctionDef:
        def __init__(self, name, description, properties, required):
            self.name = name
            self.description = description
            self.properties = properties
            self.required = required

    def sanitize_name(name):
        return name.replace("-", "_").replace(" ", "_")

logger = logging.getLogger(__name__)

def discover_and_register_tools(mcp_manager, registry) -> List['FunctionDef']:
    """Discovers tools from MCP clients and registers them with the plugin registry."""
    discovered = []

    for name, client in mcp_manager.clients.items():
        try:
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
        except Exception as e:
            logger.error(f"[MCP] Failed to discover tools for {name}: {e}")

    return discovered
