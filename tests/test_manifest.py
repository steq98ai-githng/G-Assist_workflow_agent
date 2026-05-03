import json
import os
import unittest
from unittest.mock import MagicMock

# Mock Windows dependencies for Linux testing
import ctypes
ctypes.windll = MagicMock()

# 確保路徑
_test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestManifest(unittest.TestCase):
    def test_manifest_structure(self):
        """驗證 Manifest 的基本結構與屬性。"""
        manifest_path = os.path.join(_test_dir, "manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest["version"], "4.0.4")
        self.assertEqual(manifest["protocol_version"], "2.0")
        self.assertIn("functions", manifest)
        self.assertTrue(len(manifest["functions"]) > 0)

        # Verify workflow tags
        self.assertIn("workflow", manifest["functions"][0]["tags"])
