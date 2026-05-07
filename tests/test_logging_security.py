import unittest
import asyncio
import logging
import os
import sys
import tempfile
import shutil
from unittest.mock import MagicMock

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intents.git_handler import GitIntentHandler
from intents.system_handler import SystemIntentHandler
from intents import AgentRequest

class TestLoggingSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.data_dir = self.test_dir
        self.git_handler = GitIntentHandler(self.data_dir)
        self.system_handler = SystemIntentHandler(self.data_dir)
        self.sensitive_input = "SECRET_TOKEN_12345"
        self.request = AgentRequest(user_input=self.sensitive_input)

    def test_git_handler_logging_security(self):
        """Verify GitIntentHandler does not log raw input at INFO level."""
        with self.assertLogs('intents.git_handler', level='INFO') as cm:
            async def run_handler():
                async for _ in self.git_handler.handle_stream(self.request):
                    pass
            asyncio.run(run_handler())

            # Check INFO logs
            info_logs = [log for log in cm.output if "INFO" in log]
            self.assertTrue(info_logs, "No INFO logs were captured")
            for log in info_logs:
                self.assertNotIn(self.sensitive_input, log, "Sensitive input found in INFO log!")
                self.assertIn(str(len(self.sensitive_input)), log, "Input length should be in log.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_system_handler_logging_security(self):
        """Verify SystemIntentHandler does not log raw input at INFO level."""
        with self.assertLogs('intents.system_handler', level='INFO') as cm:
            async def run_handler():
                async for _ in self.system_handler.handle_stream(self.request):
                    pass
            asyncio.run(run_handler())

            # Check INFO logs
            info_logs = [log for log in cm.output if "INFO" in log]
            for log in info_logs:
                self.assertNotIn(self.sensitive_input, log, "Sensitive input found in INFO log!")
                self.assertIn(str(len(self.sensitive_input)), log, "Input length should be in log.")

if __name__ == "__main__":
    unittest.main()
