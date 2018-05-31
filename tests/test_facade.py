import unittest
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
    pb = PubSub()

    event1_count = 0
    event2_count = 0

    def event1_handler(data):
      nonlocal event1_count
      event1_count += 1

      self.assertIsInstance(data, dict)
      self.assertEqual('Paris', data['location'])

    def event2_handler(data):
      nonlocal event2_count
      event2_count += 1

      self.assertIsInstance(data, str)
      self.assertEqual('a value', data)

    facade = TestFacadeImpl(pb, 
      on_event1=event1_handler,
      on_event2=event2_handler)

    pb.on_received('event1', '''
{
  "location": "Paris"
}
''')

    self.assertEqual(1, event1_count)
    self.assertEqual(0, event2_count)

    facade.event2()

    self.assertEqual(1, event1_count)
    self.assertEqual(1, event2_count)