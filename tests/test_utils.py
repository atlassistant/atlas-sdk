import unittest
from atlas_sdk.utils import create_instance_of, choose_one
from atlas_sdk.pubsubs.mqtt_pubsub import MQTTPubSub

class UtilsTests(unittest.TestCase):

  def test_create_instance_of(self):
    obj = create_instance_of('atlas_sdk.pubsubs.mqtt_pubsub.MQTTPubSub', host='ahost')

    self.assertIsInstance(obj, MQTTPubSub)
    self.assertEqual('ahost', obj._host)

  def test_choose_one(self):
    self.assertEqual('test', choose_one('test'))

    with_list = ['ele1', 'ele2', 'ele3']

    self.assertTrue(choose_one(with_list) in with_list)