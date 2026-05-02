import unittest
from unittest.mock import MagicMock, patch

import ctypes
ctypes.windll = MagicMock()

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.intent_router import IntentRouter, MAX_QUERY_LENGTH

class TestSecurity(unittest.TestCase):
    def test_query_length_validation(self):
        """驗證 IntentRouter 是否會拒絕超過 MAX_QUERY_LENGTH 的查詢。"""
        config = {"gemini_model": "test-model"}
        mcp_manager = MagicMock()
        registry = MagicMock()

        router = IntentRouter(config, mcp_manager, registry)

        # Test with a query that is exactly at the limit
        short_query = "a" * MAX_QUERY_LENGTH
        with patch.object(router, '_init_gemini', return_value="mock_error"): # Stop execution early
            error = router.process_query(short_query, MagicMock())
            self.assertEqual(error, "mock_error")

        # Test with a query that exceeds the limit
        long_query = "a" * (MAX_QUERY_LENGTH + 1)
        error = router.process_query(long_query, MagicMock())

        self.assertIn("查詢內容過長", error)
        self.assertIn(str(MAX_QUERY_LENGTH), error)
        self.assertIn("🛠️ 解決步驟：", error)

if __name__ == "__main__":
    unittest.main()
