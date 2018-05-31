import unittest
from atlas_sdk.utils import create_instance_of
from atlas_sdk.pubsubs.mqtt_pubsub import MQTTPubSub

class UtilsTests(unittest.TestCase):

  def test_create_instance_of(self):
    obj = create_instance_of('atlas_sdk.pubsubs.mqtt_pubsub.MQTTPubSub', host='ahost')

    self.assertIsInstance(obj, MQTTPubSub)
    self.assertEqual('ahost', obj._host)