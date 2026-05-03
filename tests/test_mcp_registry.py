import unittest
from unittest.mock import MagicMock

import ctypes
ctypes.windll = MagicMock()

import sys
import os

# 移除系統安裝的 mcp 套件（若存在），確保本地 mcp/ 目錄優先載入
for key in list(sys.modules.keys()):
    if key == "mcp" or key.startswith("mcp."):
        del sys.modules[key]

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from mcp.registry import discover_and_register_tools

class TestMCPRegistry(unittest.TestCase):
    def test_discover_and_register_tools(self):
        """驗證 MCP 動態註冊邏輯。"""
        # Mocking the client
        mock_client = MagicMock()
        mock_client.list_tools.return_value = [
            {"name": "test_tool", "description": "A test tool", "inputSchema": {}}
        ]

        # Mocking the MCP Manager
        mock_manager = MagicMock()
        mock_manager.clients = {"test_client": mock_client}
        mock_manager.tools_cache = {
            "test_client": [
                {"name": "test_tool", "description": "A test tool", "inputSchema": {}}
            ]
        }

        # Mocking the registry
        mock_registry = MagicMock()

        # Execute
        discovered = discover_and_register_tools(mock_manager, mock_registry)

        # Verify
        self.assertEqual(len(discovered), 1)
        self.assertEqual(discovered[0].name, "test_tool")
        mock_registry.register.assert_called_once()
