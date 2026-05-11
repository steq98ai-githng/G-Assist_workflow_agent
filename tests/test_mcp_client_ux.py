import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock windll for Linux environments
import ctypes
ctypes.windll = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.client import MCPManager

class TestMCPManagerUX(unittest.TestCase):
    def setUp(self):
        self.manager = MCPManager()

    def test_call_tool_not_found_ux(self):
        """驗證當找不到工具時，錯誤訊息包含正確的解決步驟。"""
        res = self.manager.call_tool("non_existent_tool", {})
        self.assertIn("❌ 找不到 MCP 工具 `non_existent_tool`。", res)
        self.assertIn("🛠️ 解決步驟：", res)
        self.assertIn("1. 執行「列出目前可用的工具」指令確認工具名稱與可用性。", res)
        self.assertIn("2. 請確認 MCP 伺服器已正確連接且狀態為運作中。", res)
        self.assertIn("3. 嘗試重新啟動外掛程式以重新載入工具清單。", res)

    def test_call_tool_execution_failed_ux(self):
        """驗證當工具執行失敗時，錯誤訊息包含正確的解決步驟與伺服器名稱。"""
        # Setup a mock client that fails
        mock_client = MagicMock()
        mock_client.call_tool.side_effect = Exception("Execution error")

        self.manager.clients["mock_server"] = mock_client
        self.manager._tool_to_client_map["failed_tool"] = "mock_server"
        self.manager.tool_maps["mock_server"] = {"failed_tool": "failed_tool_orig"}

        res = self.manager.call_tool("failed_tool", {})
        self.assertIn("❌ MCP 工具 `failed_tool` 執行失敗 (伺服器: `mock_server`)。", res)
        self.assertIn("🛠️ 解決步驟：", res)
        self.assertIn("1. 請檢查 MCP 伺服器 `mock_server` 是否正常運作。", res)
        self.assertIn("2. 嘗試執行「列出目前可用的工具」以確認工具狀態。", res)
        self.assertIn("3. 確認輸入參數是否正確。", res)

if __name__ == "__main__":
    unittest.main()
