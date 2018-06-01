import unittest, types
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub, handlers
from atlas_sdk.adapters import PubSubAdapter

class TestAdapterImpl(PubSubAdapter):
  """Sample PubSubAdapter implementation for testing only.
  """

  def __init__(self, pubsub, on_event1, on_event2):
    super(TestAdapterImpl, self).__init__(pubsub)

    pubsub.subscribe('event1', handlers.json(on_event1))
    pubsub.subscribe('event2', handlers.data(on_event2))

  def event2(self):
    self._pubsub.publish('event2', 'a value')

class AdapterTests(unittest.TestCase):

  def test_pubsub_adapter_activate(self):
    pb = PubSub()
    adapter = PubSubAdapter(pb)

    adapter.activate()
    self.assertTrue(pb.is_started())

  def test_pubsub_adapter_deactivate(self):
    pb = PubSub()
    adapter = PubSubAdapter(pb)

    adapter.activate()

    adapter.deactivate()
    self.assertFalse(pb.is_started())

  def test_pubsub_adapter_implementation(self):
    obj = types.SimpleNamespace()
    obj.event1_handler = MagicMock()
    obj.event2_handler = MagicMock()

    pb = PubSub()

    adapter = TestAdapterImpl(pb, 
      on_event1=obj.event1_handler,
      on_event2=obj.event2_handler)

    pb.on_received('event1', '''
{
  "location": "Paris"
}
''')

    obj.event1_handler.assert_called_once_with({'location': 'Paris'})
    obj.event2_handler.assert_not_called()

    adapter.event2()

    obj.event2_handler.assert_called_once_with('a value')