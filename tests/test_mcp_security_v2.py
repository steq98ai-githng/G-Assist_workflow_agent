import unittest
import os
import sys

# Mock Windows dependencies for Linux testing
from unittest.mock import MagicMock
import ctypes
ctypes.windll = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import StdioTransport, MCPError

class TestMCPSecurityFixed(unittest.TestCase):
    def test_env_filtering_fixed(self):
        """Verify that sensitive environment variables in the 'env' parameter are now filtered."""
        explicit_env = {"MY_SECRET_TOKEN": "should-be-filtered"}
        transport = StdioTransport(command=["echo", "test"], env=explicit_env)

        self.assertNotIn("MY_SECRET_TOKEN", transport._env, "Sensitive key in 'env' should be filtered")

    def test_shell_injection_blocked(self):
        """Verify that shell metacharacters like '>' are now blocked."""
        with self.assertRaises(MCPError) as cm:
            StdioTransport(command=["echo", "hello", ">", "out.txt"])
        self.assertIn("Potential shell injection detected", str(cm.exception))

    def test_newlines_blocked(self):
        """Verify that newlines in command arguments are blocked."""
        with self.assertRaises(MCPError) as cm:
            StdioTransport(command=["echo", "line1\nline2"])
        self.assertIn("Potential shell injection detected", str(cm.exception))

    def test_auth_keyword_masked(self):
        """Verify that the new 'AUTH' keyword is correctly masked in logs."""
        transport = StdioTransport(command=["login", "--auth", "secret-token"])
        masked = transport._mask_sensitive_args(transport._command)
        self.assertEqual(masked, ["login", "--auth", "********"])

    def test_auth_env_filtered(self):
        """Verify that environment variables containing 'AUTH' are filtered."""
        explicit_env = {"MY_AUTH_TOKEN": "secret"}
        transport = StdioTransport(command=["echo", "test"], env=explicit_env)
        self.assertNotIn("MY_AUTH_TOKEN", transport._env)

if __name__ == "__main__":
    unittest.main()
