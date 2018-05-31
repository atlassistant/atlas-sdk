import unittest
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.facades import ChannelFacade, topics

class ChannelFacadeTests(unittest.TestCase):

  def test_subscriptions(self):
    pb = PubSub()
    channel = ChannelFacade(pb, 'channel', 1337)
    
    channel.on_answer = MagicMock()
    channel.on_ask = MagicMock()
    channel.on_created = MagicMock()
    channel.on_destroyed = MagicMock()
    channel.on_end = MagicMock()
    channel.on_work = MagicMock()

    channel.activate()
    
    pb.on_received(topics.CHANNEL_ANSWER_TOPIC % 'channel', '{ "channel": "answer" }')
    pb.on_received(topics.CHANNEL_ANSWER_TOPIC % 'another_channel', '{ "channel": "answer" }')

    pb.on_received(topics.CHANNEL_ASK_TOPIC % 'channel', '{ "channel": "ask" }')
    pb.on_received(topics.CHANNEL_ASK_TOPIC % 'another_channel', '{ "channel": "ask" }')

    pb.on_received(topics.CHANNEL_CREATED_TOPIC % 'channel', '{ "channel": "created" }')
    pb.on_received(topics.CHANNEL_CREATED_TOPIC % 'another_channel', '{ "channel": "created" }')

    pb.on_received(topics.CHANNEL_DESTROYED_TOPIC % 'channel')
    pb.on_received(topics.CHANNEL_DESTROYED_TOPIC % 'another_channel')

    pb.on_received(topics.CHANNEL_END_TOPIC % 'channel')
    pb.on_received(topics.CHANNEL_END_TOPIC % 'another_channel')

    pb.on_received(topics.CHANNEL_WORK_TOPIC % 'channel')
    pb.on_received(topics.CHANNEL_WORK_TOPIC % 'another_channel')

    channel.on_answer.assert_called_once_with({ 'channel': 'answer' })
    channel.on_ask.assert_called_once_with({ 'channel': 'ask' })
    channel.on_created.assert_called_once_with({ 'channel': 'created' })
    channel.on_destroyed.assert_called_once()
    channel.on_end.assert_called_once()
    channel.on_work.assert_called_once()
    
  def test_publications(self):
    pb = PubSub()
    channel = ChannelFacade(pb, 'channel', 1337)

    pb.publish = MagicMock()

    channel.create()
    pb.publish.assert_called_once_with(topics.CHANNEL_CREATE_TOPIC % 'channel', '{"uid": 1337}')
    pb.publish.reset_mock()

    channel.destroy()
    pb.publish.assert_called_once_with(topics.CHANNEL_DESTROY_TOPIC % 'channel')
    pb.publish.reset_mock()

    channel.parse('a message to parse')
    pb.publish.assert_called_once_with(topics.DIALOG_PARSE_TOPIC % 'channel', "a message to parse")
