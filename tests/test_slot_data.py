import unittest
from atlas_sdk.slot_data import AttrDict, SlotData

class TestSlotData(unittest.TestCase):

  def test_attrdict(self):
    a = AttrDict({
      'location': 'Paris'
    })

    self.assertEqual('Paris', a.location)

  def test_slot_value(self):
    data = SlotData()

    self.assertFalse(data)
    self.assertIsNone(data.first().value)

    data = SlotData([{ 'value': 'a value' }, { 'value': 'another one' }, { 'value': 'a last value' }])

    self.assertTrue(data)
    self.assertEqual('a value', data.first().value)
    self.assertEqual('a last value', data.last().value)
    self.assertEqual('a value', data[0].value)
    self.assertEqual('another one', data[1].value)
