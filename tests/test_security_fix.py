import unittest
import os
import sys

# Mock Windows dependencies for Linux testing
from unittest.mock import MagicMock
import ctypes
try:
    ctypes.windll = MagicMock()
except AttributeError:
    pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import StdioTransport

class TestSecurityFix(unittest.TestCase):
    def test_sensitive_keywords_contains_auth(self):
        """Verify that AUTH is in SENSITIVE_KEYWORDS."""
        self.assertIn("AUTH", StdioTransport.SENSITIVE_KEYWORDS)

    def test_forbidden_metachars_contains_space(self):
        """Verify that space is in FORBIDDEN_METACHARS."""
        self.assertIn(" ", StdioTransport.FORBIDDEN_METACHARS)

    def test_mask_sensitive_args_logic(self):
        """Verify the masking logic for sensitive arguments."""
        transport = StdioTransport(command=["echo", "init"]) # nosec B603

        test_cases = [
            # Case 1: --key=val format
            (["cmd", "--api-key=secret123"], ["cmd", "--api-key=********"]), # nosec B105
            # Case 2: --key val format (flag triggers masking of NEXT)
            (["cmd", "--token", "secret456"], ["cmd", "--token", "********"]), # nosec B105
            # Case 3: Standalone sensitive value (not a flag) should be masked IMMEDIATELY
            (["cmd", "secret789_TOKEN"], ["cmd", "********"]), # nosec B105
            # Case 4: AUTH keyword (newly added)
            (["cmd", "--auth-token=secretABC"], ["cmd", "--auth-token=********"]), # nosec B105
            # Case 5: Normal args
            (["cmd", "arg1", "arg2"], ["cmd", "arg1", "arg2"]),
            # Case 6: Non-flag containing keyword does NOT mask next arg
            (["cmd", "MY_TOKEN_VALUE", "safe_arg"], ["cmd", "********", "safe_arg"]), # nosec B105
        ]

        for input_args, expected_output in test_cases:
            with self.subTest(input_args=input_args):
                masked = transport._mask_sensitive_args(input_args)
                self.assertEqual(masked, expected_output)

if __name__ == "__main__":
    unittest.main()
