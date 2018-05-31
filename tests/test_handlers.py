import unittest
from atlas_sdk.pubsubs.handlers import json, data, empty

class HandlersTests(unittest.TestCase):

  def test_json(self):
    handler_called = False
    
    def my_handler(data):
      nonlocal handler_called

      handler_called = True

      self.assertIsInstance(data, dict)
      self.assertEqual('Paris', data['location'])

    handler = json(my_handler)
    handler('event1', '''
{
  "location": "Paris"
}
''')

    self.assertTrue(handler_called)

  def test_empty(self):
    handler_called = False

    def my_handler():
      nonlocal handler_called
      handler_called = True

    handler = empty(my_handler)
    handler('event1', 'raw value')

    self.assertTrue(handler_called)

  def test_data(self):
    handler_called = False
    
    def my_handler(data):
      nonlocal handler_called

      handler_called = True
      
      self.assertIsInstance(data, str)
      self.assertEqual('raw value', data)

    handler = data(my_handler)
    handler('event1', 'raw value')

    self.assertTrue(handler_called)

    