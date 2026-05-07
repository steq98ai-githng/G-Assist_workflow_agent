import unittest
import os
import sys

# Mock Windows dependencies for Linux testing
from unittest.mock import MagicMock
import ctypes
ctypes.windll = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import StdioTransport

class TestStdioTransport(unittest.TestCase):
    def test_mask_sensitive_args(self):
        """Verify that sensitive command line arguments are correctly masked."""
        transport = StdioTransport(command=["echo", "test"])

        test_cases = [
            (["--auth", "SECRET_TOKEN"], ["--auth", "********"]),
            (["Token:secret", "--other", "val"], ["********", "--other", "val"]),
            (["--api-key=secret"], ["--api-key=********"]),
            (["--password"], ["********"]),
            (["--Authorization", "Bearer xyz"], ["--Authorization", "********"]),
            (["--header=Authorization: Bearer xyz"], ["--header=********"]),
            (["--token", "t1", "--secret", "s1"], ["--token", "********", "--secret", "********"]),
        ]

        for args, expected in test_cases:
            with self.subTest(args=args):
                masked = transport._mask_sensitive_args(args)
                self.assertEqual(masked, expected)

    def test_environment_variable_sanitization(self):
        """Verify that sensitive environment variables are filtered out of the subprocess environment."""

        # Backup original environment
        original_environ = os.environ.copy()

        try:
            # Set up a fake environment with both sensitive and safe variables
            os.environ.clear()
            os.environ["SAFE_VAR"] = "safe_value"
            os.environ["PATH"] = "/usr/bin"
            os.environ["MY_API_KEY"] = "super_secret"  # nosec B105
            os.environ["GITHUB_TOKEN"] = "token_123"  # nosec B105
            os.environ["DB_PASSWORD"] = "password456"  # nosec B105
            os.environ["AWS_SECRET_ACCESS_KEY"] = "aws_secret"  # nosec B105
            os.environ["USER_CREDENTIALS"] = "creds_789"  # nosec B105

            # Explicitly passed safe env override
            explicit_env = {"EXPLICIT_VAR": "explicit_value"}

            # Initialize transport
            transport = StdioTransport(command=["echo", "test"], env=explicit_env)

            # Check the sanitized environment passed to subprocess
            subprocess_env = transport._env

            # Safe vars should exist
            self.assertIn("SAFE_VAR", subprocess_env)
            self.assertEqual(subprocess_env["SAFE_VAR"], "safe_value")

            self.assertIn("PATH", subprocess_env)
            self.assertEqual(subprocess_env["PATH"], "/usr/bin")

            # Explicit env should exist
            self.assertIn("EXPLICIT_VAR", subprocess_env)
            self.assertEqual(subprocess_env["EXPLICIT_VAR"], "explicit_value")

            # Sensitive vars should be filtered out
            self.assertNotIn("MY_API_KEY", subprocess_env)
            self.assertNotIn("GITHUB_TOKEN", subprocess_env)
            self.assertNotIn("DB_PASSWORD", subprocess_env)
            self.assertNotIn("AWS_SECRET_ACCESS_KEY", subprocess_env)
            self.assertNotIn("USER_CREDENTIALS", subprocess_env)

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_environ)

if __name__ == "__main__":
    unittest.main()
