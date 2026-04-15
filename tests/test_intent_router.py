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
            self.assertIn("請設定 GEMINI_API_KEY", error)
