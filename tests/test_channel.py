import unittest, types
from unittest.mock import MagicMock
from datetime import timedelta
from unittest.mock import MagicMock
from atlas_sdk.channel import Channel
from atlas_sdk.adapters import ChannelAdapter
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.constants import STARTED_AT_KEY

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

    channel.on_created({ 'lang': 'fr' })

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

  def test_custom_handlers(self):
    obj = types.SimpleNamespace()
    obj.on_created = MagicMock()
    obj.on_destroyed = MagicMock()
    obj.on_ask = MagicMock()
    obj.on_answer = MagicMock()
    obj.on_end = MagicMock()
    obj.on_work = MagicMock()

    pb = PubSub()
    adapter = ChannelAdapter(pb)
    
    channel = Channel('sid', 'uid', adapter, 
      on_created=obj.on_created,
      on_destroyed=obj.on_destroyed,
      on_answer=obj.on_answer,
      on_ask=obj.on_ask,
      on_end=obj.on_end,
      on_work=obj.on_work)

    adapter.on_created({ 'lang': 'fr' })
    adapter.on_destroyed()
    adapter.on_end()
    adapter.on_work()
    adapter.on_answer({})
    adapter.on_ask({})

    obj.on_created.assert_called_once_with({'lang': 'fr'})
    obj.on_destroyed.assert_called_once()
    obj.on_end.assert_called_once()
    obj.on_work.assert_called_once()
    obj.on_answer.assert_called_once_with({})
    obj.on_ask.assert_called_once_with({})