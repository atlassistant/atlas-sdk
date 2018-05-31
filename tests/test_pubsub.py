import unittest
from atlas_sdk.pubsubs import PubSub

class PubSubTests(unittest.TestCase):

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

  def test_on_received(self):
    pb = PubSub()

    event1_count = 0
    event2_count = 0

    def event1_handler(topic, data):
      nonlocal event1_count
      event1_count+=1

      self.assertEqual('event1', topic)
      self.assertEqual('data1', data)

    def event1_handler2(topic, data):
      nonlocal event1_count
      event1_count+=1

      self.assertEqual('event1', topic)
      self.assertEqual('data1', data)

    def event2_handler(topic, data):
      nonlocal event2_count
      event2_count+=1

      self.assertEqual('event2', topic)
      self.assertEqual('data2', data)

    pb.subscribe('event1', event1_handler)
    pb.subscribe('event1', event1_handler2)
    pb.subscribe('event2', event2_handler)

    pb.on_received('event1', 'data1')
    pb.on_received('event2', 'data2')

    self.assertEqual(2, event1_count)
    self.assertEqual(1, event2_count)
