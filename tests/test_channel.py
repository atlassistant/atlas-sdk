import unittest, types
from unittest.mock import MagicMock, patch, mock_open
from datetime import timedelta
from atlas_sdk.channel import Channel
from atlas_sdk.adapters import ChannelAdapter
from atlas_sdk.pubsubs import PubSub

class ChannelTests(unittest.TestCase):

  @patch('builtins.open')
  def test_from_config(self, m_open):
    m_open.side_effect = [
      mock_open(read_data='''
channel:
  id: my_channel
messaging:
  host: 127.0.0.1
''').return_value
    ]

    channel = Channel.from_config('conf.yml')

    self.assertEqual('my_channel', channel._adapter._channel_id)
    self.assertEqual('127.0.0.1', channel._adapter._pubsub._host)

  def test_with(self):
    pb = PubSub()
    adapter = ChannelAdapter(pb)
    channel = Channel('a channel', adapter=adapter)

    with channel:
      self.assertTrue(channel._adapter._pubsub.is_started())

    self.assertFalse(channel._adapter._pubsub.is_started())

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