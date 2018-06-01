import unittest
from datetime import timedelta
from unittest.mock import MagicMock
from atlas_sdk.channel import Channel
from atlas_sdk.adapters import ChannelAdapter
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.keys import STARTED_AT_KEY

class ChannelTests(unittest.TestCase):

  def test_created(self):
    pb = PubSub()
    adapter = ChannelAdapter(pb)
    channel = Channel('sid', 'uid', adapter)

    self.assertIsNone(channel.lang())
    self.assertIsNone(channel._created_at)

    channel.on_created({
      'lang': 'fr'
    })

    self.assertEqual('fr', channel.lang())
    self.assertIsNotNone(channel._created_at)

  def test_check_still_connected(self):
    pb = PubSub()
    adapter = ChannelAdapter(pb)
    adapter.create = MagicMock()
    channel = Channel('sid', 'uid', adapter)

    self.assertIsNone(channel._created_at)

    channel.on_created({
      'lang': 'fr'
    })

    self.assertIsNotNone(channel._created_at)

    channel.check_still_connected({})

    adapter.create.assert_not_called()

    # Server created before, nothing has changed

    channel.check_still_connected({
      STARTED_AT_KEY: (channel._created_at - timedelta(seconds=5)).isoformat()
    })

    adapter.create.assert_not_called()

    # Server created after, it must call create

    channel.check_still_connected({
      STARTED_AT_KEY: (channel._created_at + timedelta(seconds=5)).isoformat()
    })

    adapter.create.assert_called_once()