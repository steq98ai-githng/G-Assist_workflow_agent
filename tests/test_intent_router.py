import unittest
from unittest.mock import MagicMock, patch

import ctypes
ctypes.windll = MagicMock()

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.intent_router import IntentRouter

class TestIntentRouter(unittest.TestCase):
    @patch.dict('sys.modules', {'google': MagicMock(), 'google.genai': MagicMock()})
    def test_init_gemini_missing_key(self):
        """驗證 Gemini 缺少 API Key 的處理邏輯。"""
        config = {"gemini_model": "test-model"}
        mcp_manager = MagicMock()
        registry = MagicMock()
        registry.plugin_dir = "/dummy"

        router = IntentRouter(config, mcp_manager, registry)

        with patch.dict('os.environ', clear=True):
            error = router._init_gemini()
            self.assertIn("缺少 Gemini API Key", error)
            self.assertIn("🛠️ 解決步驟：", error)

    @patch.dict('sys.modules', {'google': MagicMock()})
    def test_init_gemini_import_error(self):
        """驗證 Gemini 缺少套件時的回應。"""
        config = {"gemini_model": "test-model"}
        mcp_manager = MagicMock()
        registry = MagicMock()

        router = IntentRouter(config, mcp_manager, registry)

        with patch.dict('os.environ', {'GEMINI_API_KEY': 'dummy'}):
            import sys
            import google
            # Mock google module so that 'from google import genai' fails
            # We can override google to not have genai
            if hasattr(google, 'genai'):
                delattr(google, 'genai')
            # remove from sys.modules if exists
            if 'google.genai' in sys.modules:
                del sys.modules['google.genai']

            # Use mock for the import exception inside the method
            with patch('builtins.__import__', side_effect=ImportError("No module named 'google.genai'")):
                error = router._init_gemini()
                self.assertIn("缺少 google-genai SDK 套件", error)
                self.assertIn("🛠️ 解決步驟：", error)

    @patch.dict('sys.modules', {'google': MagicMock(), 'google.genai': MagicMock()})
    def test_init_gemini_general_exception(self):
        """驗證 Gemini 初始化發生其他例外時的回應。"""
        config = {"gemini_model": "test-model"}
        mcp_manager = MagicMock()
        registry = MagicMock()

        router = IntentRouter(config, mcp_manager, registry)

        with patch.dict('os.environ', {'GEMINI_API_KEY': 'dummy'}):
            import google.genai
            # Mock genai.Client to raise a general Exception
            google.genai.Client = MagicMock(side_effect=Exception("Network failed"))
            error = router._init_gemini()
            self.assertIn("Gemini 引擎初始化失敗", error)
            self.assertIn("🛠️ 解決步驟：", error)

    def test_process_query_too_long(self):
        """驗證查詢內容過長時的處理邏輯。"""
        config = {"gemini_model": "test-model"}
        mcp_manager = MagicMock()
        registry = MagicMock()

        router = IntentRouter(config, mcp_manager, registry)
        long_query = "A" * (router.MAX_QUERY_LENGTH + 1)

        # We don't need to mock genai here because the length check happens before initialization
        error = router.process_query(long_query, MagicMock())
        self.assertIn("查詢內容過長", error)
        self.assertIn(f"上限 {router.MAX_QUERY_LENGTH:,} 字元", error)
