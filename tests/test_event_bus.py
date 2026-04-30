import unittest
from unittest.mock import MagicMock
from core.event_bus import EventBus

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()

    def test_subscribe(self):
        """Verify that subscribing correctly registers a callback function."""
        def callback(): pass
        self.bus.subscribe("test_event", callback)
        self.assertIn("test_event", self.bus.subscribers)
        self.assertIn(callback, self.bus.subscribers["test_event"])

    def test_publish_single_subscriber(self):
        """Verify that a single subscriber is called when its event is published."""
        callback = MagicMock()
        self.bus.subscribe("test_event", callback)
        self.bus.publish("test_event")
        callback.assert_called_once()

    def test_publish_multiple_subscribers(self):
        """Verify that all subscribers are called when their event is published."""
        callback1 = MagicMock()
        callback2 = MagicMock()
        self.bus.subscribe("test_event", callback1)
        self.bus.subscribe("test_event", callback2)
        self.bus.publish("test_event")
        callback1.assert_called_once()
        callback2.assert_called_once()

    def test_publish_with_args_kwargs(self):
        """Verify that arguments and keyword arguments are correctly passed to callbacks."""
        callback = MagicMock()
        self.bus.subscribe("test_event", callback)
        self.bus.publish("test_event", "arg1", key1="value1")
        callback.assert_called_once_with("arg1", key1="value1")

    def test_publish_no_subscribers(self):
        """Verify that publishing an event with no subscribers does not raise an error."""
        # Should not raise any exception
        self.bus.publish("non_existent_event")

    def test_multiple_event_types(self):
        """Verify that subscribers of different event types are isolated."""
        callback_a = MagicMock()
        callback_b = MagicMock()
        self.bus.subscribe("event_a", callback_a)
        self.bus.subscribe("event_b", callback_b)

        self.bus.publish("event_a")
        callback_a.assert_called_once()
        callback_b.assert_not_called()

        callback_a.reset_mock()
        self.bus.publish("event_b")
        callback_a.assert_not_called()
        callback_b.assert_called_once()
