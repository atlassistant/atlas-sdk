import unittest
from unittest.mock import MagicMock
from atlas_sdk.config import Config
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.adapters import SkillAdapter
from atlas_sdk.request import Request
from atlas_sdk.topics import DIALOG_END_TOPIC, DIALOG_ANSWER_TOPIC, DIALOG_ASK_TOPIC

class RequestTests(unittest.TestCase):

  def test_init(self):
    pb = PubSub()
    adapter = SkillAdapter(pb)

    data = {
      '__sid': 'session_id',
      '__uid': 'user_id',
      '__cid': 'conversation_id',
      '__lang': 'fr',
      '__settings': {
        'aparam': 'avalue'
      }
    }

    request = Request(adapter, data)

    self.assertEqual('session_id', request.session_id)
    self.assertEqual('user_id', request.user_id)
    self.assertEqual('conversation_id', request.conversation_id)
    self.assertEqual('fr', request.lang)
    self.assertIsInstance(request.settings, Config)
    self.assertEqual('avalue', request.settings.get('aparam'))
    self.assertEqual(data, request._data)

  def test_slot(self):
    pb = PubSub()
    adapter = SkillAdapter(pb)

    data = {
      'location': [{
        'value': 'Paris'
      }, {
        'value': 'London'
      }]
    }

    request = Request(adapter, data)
    self.assertEqual('Paris', request.slot('location').first().value)
    self.assertEqual('London', request.slot('location').last().value)

  def test_end(self):
    pb = PubSub()
    pb.publish = MagicMock()

    adapter = SkillAdapter(pb)
    request = Request(adapter, { '__cid': 'conversation_id' })

    request.end()

    pb.publish.assert_called_once_with(DIALOG_END_TOPIC, '{"__cid": "conversation_id"}')

  def test_ask(self):
    pb = PubSub()
    pb.publish = MagicMock()

    adapter = SkillAdapter(pb)
    request = Request(adapter, { '__cid': 'conversation_id' })

    request.ask('location', 'Choose a location')

    pb.publish.assert_called_once_with(DIALOG_ASK_TOPIC, '{"__cid": "conversation_id", "slot": "location", "text": "Choose a location", "choices": null}')
    pb.publish.reset_mock()

    request.ask('location', 'Choose a location', choices=['Paris', 'London'])
    pb.publish.assert_called_once_with(DIALOG_ASK_TOPIC, '{"__cid": "conversation_id", "slot": "location", "text": "Choose a location", "choices": ["Paris", "London"]}')

  def test_answer(self):
    pb = PubSub()
    pb.publish = MagicMock()

    adapter = SkillAdapter(pb)
    request = Request(adapter, { '__cid': 'conversation_id' })

    request.answer('hello')

    pb.publish.assert_called_once_with(DIALOG_ANSWER_TOPIC, '{"__cid": "conversation_id", "text": "hello", "cards": null}')
    pb.publish.reset_mock()

    request.answer('hello with end', end_conversation=True)

    pb.publish.assert_any_call(DIALOG_ANSWER_TOPIC, '{"__cid": "conversation_id", "text": "hello with end", "cards": null}')
    pb.publish.assert_any_call(DIALOG_END_TOPIC, '{"__cid": "conversation_id"}')