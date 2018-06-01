import unittest, types
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub, handlers
from atlas_sdk.facades import PubSubFacade

class TestFacadeImpl(PubSubFacade):
  """Sample PubSubFacade implementation for testing only.
  """

  def __init__(self, pubsub, on_event1, on_event2):
    super(TestFacadeImpl, self).__init__(pubsub)

    pubsub.subscribe('event1', handlers.json(on_event1))
    pubsub.subscribe('event2', handlers.data(on_event2))

  def event2(self):
    self._pubsub.publish('event2', 'a value')

class FacadeTests(unittest.TestCase):

  def test_pubsub_facade_activate(self):
    pb = PubSub()
    facade = PubSubFacade(pb)

    facade.activate()
    self.assertTrue(pb.is_started())

  def test_pubsub_facade_deactivate(self):
    pb = PubSub()
    facade = PubSubFacade(pb)

    facade.activate()

    facade.deactivate()
    self.assertFalse(pb.is_started())

  def test_pubsub_facade_implementation(self):
    obj = types.SimpleNamespace()
    obj.event1_handler = MagicMock()
    obj.event2_handler = MagicMock()

    pb = PubSub()

    facade = TestFacadeImpl(pb, 
      on_event1=obj.event1_handler,
      on_event2=obj.event2_handler)

    pb.on_received('event1', '''
{
  "location": "Paris"
}
''')

    obj.event1_handler.assert_called_once_with({'location': 'Paris'})
    obj.event2_handler.assert_not_called()

    facade.event2()

    obj.event2_handler.assert_called_once_with('a value')