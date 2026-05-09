import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock Windows dependencies for Linux testing
import ctypes
try:
    ctypes.windll = MagicMock()
except AttributeError:
    pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import StdioTransport, MCPError

class TestSentinelReproduction(unittest.TestCase):
    def setUp(self):
        # We don't need a real process, just the transport object
        self.transport = StdioTransport(command=["echo", "init"])

    def test_mask_sensitive_args_standalone(self):
        """Verify that standalone sensitive values are correctly masked."""
        args = ["server", "TOKEN_12345", "normal_arg"]
        masked = self.transport._mask_sensitive_args(args)

        self.assertEqual(masked[1], "********", f"Standalone token should be masked, but got {masked[1]}")
        self.assertEqual(masked[2], "normal_arg", f"Subsequent arg should NOT be masked, but got {masked[2]}")

    def test_mask_sensitive_args_flag_format(self):
        """Ensure flag format --token value still works."""
        args = ["server", "--token", "secret_val"]
        masked = self.transport._mask_sensitive_args(args)

        self.assertEqual(masked[1], "--token")
        self.assertEqual(masked[2], "********")

    def test_space_blocked(self):
        """Confirm that space IS in FORBIDDEN_METACHARS and blocks command initialization."""
        with self.assertRaises(MCPError) as cm:
            StdioTransport(command=["echo", "name with space"])
        self.assertIn("Potential shell injection detected", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
