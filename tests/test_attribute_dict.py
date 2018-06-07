import unittest
from atlas_sdk.attribute_dict import AttributeDict

class AttributeDictTests(unittest.TestCase):
  
  def test_attribute_access(self):
    d = AttributeDict({ 'prop': 'value', 'dict': { 'prop': 'value_in' } })

    self.assertEqual('value', d.prop)
    self.assertEqual('value_in', d.dict.prop)

    self.assertIsNone(d.not_exist)

  def test_empty(self):
    d = AttributeDict()
    