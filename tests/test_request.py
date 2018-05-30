import unittest
from atlas_sdk.request import Request

class TestRequest(unittest.TestCase):
  
  def test_slot(self):
    req = Request(None, { }, None)
    data = req.slot('location')

    self.assertIsNotNone(data)
    self.assertIsNone(data.first().value)

    req = Request(None, {
      'location': [{ 'value': 'Paris' }]
    }, None)

    data = req.slot('location')

    self.assertEqual('Paris', data.first().value)