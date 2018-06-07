import unittest
from atlas_sdk.slot_data import SlotData

class SlotDataTests(unittest.TestCase):
    
  def test_empty(self):
    data = SlotData()

    self.assertEqual(0, len(data))
  
  def test_get(self):
    data = SlotData([{ 'one': 1 }, { 'two': 2 }])

    self.assertEqual(1, data[0].one)
    self.assertEqual(2, data[1].two)

  def test_first(self):
    data = SlotData([{ 'value': 'a value' }, { 'value': 'another one' }, { 'value': 'a last value' }])

    self.assertEqual('a value', data.first().value)

  def test_last(self):
    data = SlotData([{ 'value': 'a value' }, { 'value': 'another one' }, { 'value': 'a last value' }])

    self.assertEqual('a last value', data.last().value)