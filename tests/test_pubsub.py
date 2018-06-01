import unittest, types
from unittest.mock import MagicMock
from atlas_sdk.config import config
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.pubsubs.mqtt_pubsub import MQTTPubSub

class PubSubTests(unittest.TestCase):

  def test_from_config(self):
    pb = PubSub.from_config()

    self.assertIsInstance(pb, PubSub)
    self.assertIsInstance(pb, MQTTPubSub)

    config.update({
      'messaging': {
        'type': 'atlas_sdk.pubsubs.mqtt_pubsub.MQTTPubSub',
        'host': 'localhost',
        'port': 5555
      }
    })

    pb = PubSub.from_config()

    self.assertIsInstance(pb, PubSub)
    self.assertIsInstance(pb, MQTTPubSub)

    self.assertEqual(5555, pb._port)

    config.update({
      'messaging': {
        'type': 'atlas_sdk.pubsubs.PubSub',
      }
    })

    pb = PubSub.from_config()
    self.assertIsInstance(pb, PubSub)
    self.assertNotIsInstance(pb, MQTTPubSub)

  def test_init(self):
    pb = PubSub()

    self.assertEqual({}, pb._handlers)
    self.assertFalse(pb.is_started())

  def test_start_stop(self):
    pb = PubSub()

    pb.start()
    self.assertTrue(pb.is_started())
    
    pb.stop()
    self.assertFalse(pb.is_started())

  def test_subscribe(self):
    pb = PubSub()

    def handler(topic, data):
      pass

    pb.subscribe('event1', handler)
    pb.subscribe('event1', handler)
    pb.subscribe('event2', handler)

    self.assertEqual(2, len(pb._handlers))
    self.assertEqual(2, len(pb._handlers['event1']))
    self.assertEqual(1, len(pb._handlers['event2']))
    self.assertEqual(handler, pb._handlers['event1'][0])

  def test_unsubscribe(self):
    obj = types.SimpleNamespace()
    obj.event1_handler = MagicMock()
    obj.event2_handler = MagicMock()

    pb = PubSub()

    pb.subscribe('event1', obj.event1_handler)
    pb.subscribe('event2', obj.event2_handler)

    self.assertEqual(2, len(pb._handlers))

    pb.unsubscribe('event1')

    self.assertEqual(1, len(pb._handlers))
    self.assertFalse('event1' in pb._handlers)

    pb.on_received('event1', 'data1')
    pb.on_received('event2', 'data2')

    obj.event1_handler.assert_not_called()
    obj.event2_handler.assert_called_once_with('event2', 'data2')

  def test_on_received(self):
    obj = types.SimpleNamespace()
    obj.event1_handler = MagicMock()
    obj.event1_handler2 = MagicMock()
    obj.event2_handler = MagicMock()

    pb = PubSub()

    pb.subscribe('event1', obj.event1_handler)
    pb.subscribe('event1', obj.event1_handler2)
    pb.subscribe('event2', obj.event2_handler)

    pb.on_received('event1', 'data1')
    pb.on_received('event2', 'data2')

    obj.event1_handler.assert_called_once_with('event1', 'data1')
    obj.event1_handler2.assert_called_once_with('event1', 'data1')
    obj.event2_handler.assert_called_once_with('event2', 'data2')
