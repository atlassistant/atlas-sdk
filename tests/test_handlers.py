import unittest, types, logging
from unittest.mock import MagicMock
from atlas_sdk.pubsubs.handlers import json, data, empty, notset

class HandlersTests(unittest.TestCase):

  def test_json(self):
    obj = types.SimpleNamespace()
    obj.handler = MagicMock()

    handler = json(obj.handler)
    handler('event1', '''
{
  "location": "Paris"
}
''')

    obj.handler.assert_called_once_with({'location': 'Paris'})

  def test_empty(self):
    obj = types.SimpleNamespace()
    obj.handler = MagicMock()

    handler = empty(obj.handler)
    handler('event1', 'raw value')

    obj.handler.assert_called_once_with()

  def test_data(self):
    obj = types.SimpleNamespace()
    obj.handler = MagicMock()

    handler = data(obj.handler)
    handler('event1', 'raw value')

    obj.handler.assert_called_once_with('raw value')

  def test_notset(self):
    obj = types.SimpleNamespace()
    obj.handler = MagicMock()

    handler = notset(logging)
    handler('event1', 'a value')
    

    