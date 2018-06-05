import unittest, types
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.topics import DISCOVERY_PING_TOPIC
from atlas_sdk.pubsubs.constants import ON_CONNECTED_TOPIC
from atlas_sdk.adapters.skill_adapter import SkillAdapter

class SkillAdapterTests(unittest.TestCase):

  def test_attach(self):
    pb = PubSub()
    data = {
      'name': 'A skill',
      'version': '1.0.0',
    }

    skill = SkillAdapter(pb)
    skill.attach(data)

    self.assertEqual(data, skill._skill_data)

  def test_subscriptions(self):
    obj = types.SimpleNamespace()
    obj.handler1 = MagicMock()
    obj.handler2 = MagicMock()

    pb = PubSub()

    skill = SkillAdapter(pb)
    skill.attach({
      'intents': {
        'something': None,
        'somethingElse': None
      }
    })

    skill.pong = MagicMock()
    skill.on_discovery_ping = MagicMock()

    skill.handle('something', obj.handler1)
    skill.handle('somethingElse', obj.handler2)

    skill.activate()

    pb.on_received(ON_CONNECTED_TOPIC)

    skill.pong.assert_called_once();
    skill.on_discovery_ping.assert_not_called();

    pb.on_received(DISCOVERY_PING_TOPIC, '{ "version": "1.0.0" }')
    skill.on_discovery_ping.assert_called_once_with({ 'version': '1.0.0' });

    pb.on_received('something', '{"cid": "conversation_id"}')

    obj.handler1.assert_called_once_with({'cid': 'conversation_id'})
    obj.handler2.assert_not_called()

    pb.on_received('somethingElse', '{"cid": "conversation_id2"}')

    obj.handler1.assert_called_once()
    obj.handler2.assert_called_once_with({'cid': 'conversation_id2'})

  def test_unsubscriptions(self):
    pass

  def test_publications(self):
    pass