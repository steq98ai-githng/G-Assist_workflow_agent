import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock Windows dependencies for Linux testing
import ctypes
ctypes.windll = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import StdioTransport, MCPError

class TestMCPMaskingFix(unittest.TestCase):
    def test_space_blocking(self):
        """Verify that space characters in command arguments are now blocked."""
        with self.assertRaises(MCPError) as cm:
            StdioTransport(command=["echo", "argument with spaces"])
        self.assertIn("Potential shell injection detected", str(cm.exception))

    def test_improved_masking_logic(self):
        """Verify the improved masking logic handles various cases correctly."""
        transport = StdioTransport(command=["node", "server.js"])

        # Test Case 1: --key=val
        args1 = ["--api-key=secret123"]
        self.assertEqual(transport._mask_sensitive_args(args1), ["--api-key=********"])

        # Test Case 2: --key val (Flag follows keyword)
        args2 = ["--api-key", "secret456"]
        self.assertEqual(transport._mask_sensitive_args(args2), ["--api-key", "********"])

        # Test Case 3: Standalone sensitive value containing keyword
        args3 = ["MY_TOKEN_789"]
        self.assertEqual(transport._mask_sensitive_args(args3), ["********"])

        # Test Case 4: AUTH keyword
        args4 = ["--auth-token", "auth123"]
        self.assertEqual(transport._mask_sensitive_args(args4), ["--auth-token", "********"])

        # Test Case 5: Keyword in positional arg (should NOT trigger masking of NEXT arg)
        # Previously, if "TOKEN" was in a positional arg, it might skip the next arg.
        # Now it should mask itself but not the next one.
        args5 = ["SOME_TOKEN", "safe_arg"]
        self.assertEqual(transport._mask_sensitive_args(args5), ["********", "safe_arg"])

        # Test Case 6: Mixed cases
        args6 = ["--user", "jules", "--password", "pass123", "extra"]
        self.assertEqual(transport._mask_sensitive_args(args6), ["--user", "jules", "--password", "********", "extra"])

if __name__ == "__main__":
    unittest.main()
