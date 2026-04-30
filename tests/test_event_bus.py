import unittest
from unittest.mock import MagicMock
import os
import sys

# Project convention for module resolution
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()

    def test_subscribe_and_publish(self):
        mock_callback = MagicMock()
        self.bus.subscribe("test_event", mock_callback)

        self.bus.publish("test_event", "arg1", key="val")

        mock_callback.assert_called_once_with("arg1", key="val")

    def test_multiple_subscribers(self):
        callback1 = MagicMock()
        callback2 = MagicMock()

        self.bus.subscribe("event", callback1)
        self.bus.subscribe("event", callback2)

        self.bus.publish("event", "test_arg", key="test_val")

        callback1.assert_called_once_with("test_arg", key="test_val")
        callback2.assert_called_once_with("test_arg", key="test_val")

    def test_publish_no_subscribers(self):
        # Should not raise exception
        self.bus.publish("non_existent_event")

    def test_separate_events(self):
        callback1 = MagicMock()
        callback2 = MagicMock()

        self.bus.subscribe("event1", callback1)
        self.bus.subscribe("event2", callback2)

        self.bus.publish("event1")

        callback1.assert_called_once()
        callback2.assert_not_called()

if __name__ == "__main__":
    unittest.main()
