import unittest
from unittest.mock import MagicMock

import ctypes
ctypes.windll = MagicMock()

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

        # Mocking the registry
        mock_registry = MagicMock()

        # Execute
        discovered = discover_and_register_tools(mock_manager, mock_registry)

        # Verify
        self.assertEqual(len(discovered), 1)
        self.assertEqual(discovered[0].name, "test_tool")
        mock_registry.register.assert_called_once()
