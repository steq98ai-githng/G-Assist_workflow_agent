import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import logging

# Mock Windows dependencies for Linux testing
import ctypes
ctypes.windll = MagicMock()

# Mock requests before importing mcp to bypass ImportError
mock_requests = MagicMock()
sys.modules["requests"] = mock_requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import HTTPTransport, HAS_REQUESTS

class TestMCPSecurity(unittest.TestCase):
    def test_verify_false_logs_warning(self):
        """Verify that passing verify=False to HTTPTransport logs a security warning."""
        with self.assertLogs("gassist_sdk.mcp", level="WARNING") as cm:
            HTTPTransport(url="https://example.com/mcp", verify=False)

        self.assertTrue(any("SSL verification is disabled" in output for output in cm.output))
        self.assertTrue(any("security risk" in output.lower() for output in cm.output))

    def test_verify_true_no_warning(self):
        """Verify that passing verify=True to HTTPTransport does not log the security warning."""
        # Use patch to check that warning was NOT called with the security message
        with patch("libs.gassist_sdk.mcp.logger.warning") as mock_warning:
            HTTPTransport(url="https://example.com/mcp", verify=True)

            # Check all calls to warning
            for args, kwargs in mock_warning.call_args_list:
                msg = args[0] if args else ""
                self.assertNotIn("SSL verification is disabled", msg)

if __name__ == "__main__":
    unittest.main()
