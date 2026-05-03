import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Mock Windows dependencies for Linux testing
from unittest.mock import MagicMock
import ctypes
ctypes.windll = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gassist_sdk.mcp import StdioTransport

class TestStdioTransport(unittest.TestCase):
    def test_log_redaction(self):
        """Verify that sensitive command arguments are redacted in logs."""
        from libs.gassist_sdk.mcp import logger

        # Test command with sensitive info
        command = ["my-server", "--api-key", "v1.real_key", "--token=abc", "safe-arg"]

        with patch.object(logger, 'info') as mock_info:
            # Mock subprocess.Popen to avoid actually running anything
            with patch('subprocess.Popen') as mock_popen:
                mock_popen.return_value.poll.return_value = None

                transport = StdioTransport(command=command)
                transport.start()

                # Check that the log message exists and is redacted
                self.assertTrue(mock_info.called)
                log_msg = mock_info.call_args[0][0]

                self.assertIn("Started MCP server:", log_msg)
                self.assertIn("my-server", log_msg)
                self.assertIn("safe-arg", log_msg)
                self.assertIn("[REDACTED]", log_msg)
                self.assertNotIn("v1.real_key", log_msg)
                self.assertNotIn("abc", log_msg)

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
