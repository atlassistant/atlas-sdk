import unittest, types
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.topics import ATLAS_STATUS_LOADED, ATLAS_REGISTRY_SKILL, DIALOG_END_TOPIC, \
  DIALOG_ANSWER_TOPIC, DIALOG_ASK_TOPIC, INTENT_TOPIC, ATLAS_STATUS_UNLOADED
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

    skill.register = MagicMock()
    skill.on_atlas_loaded = MagicMock()
    skill.on_atlas_unloaded = MagicMock()

    skill.handle('something', obj.handler1)
    skill.handle('somethingElse', obj.handler2)

    skill.activate()

    pb.on_received(ON_CONNECTED_TOPIC)

    skill.register.assert_called_once();
    skill.register.reset_mock()

    pb.on_received(ATLAS_STATUS_LOADED, '{ "version": "1.0.0" }')
    skill.register.assert_called_once_with({ 'version': '1.0.0' });
    skill.on_atlas_loaded.assert_called_once_with({ 'version': '1.0.0' });

    pb.on_received(ATLAS_STATUS_UNLOADED)
    skill.on_atlas_unloaded.assert_called_once_with();

    pb.on_received(INTENT_TOPIC % 'something', '{"cid": "conversation_id"}')

    obj.handler1.assert_called_once_with({'cid': 'conversation_id'})
    obj.handler2.assert_not_called()

    pb.on_received(INTENT_TOPIC % 'somethingElse', '{"cid": "conversation_id2"}')

    obj.handler1.assert_called_once()
    obj.handler2.assert_called_once_with({'cid': 'conversation_id2'})

  def test_unsubscriptions(self):
    obj = types.SimpleNamespace()
    obj.intent1_handler = MagicMock()
    obj.intent2_handler = MagicMock()

    pb = PubSub()
    skill = SkillAdapter(pb)

    skill.handle('intent1', obj.intent1_handler)
    skill.handle('intent2', obj.intent2_handler)

    self.assertTrue(INTENT_TOPIC % 'intent1' in skill._pubsub._handlers)
    self.assertTrue(INTENT_TOPIC % 'intent2' in skill._pubsub._handlers)
    
    skill.deactivate()

    self.assertFalse(INTENT_TOPIC % 'intent1' in skill._pubsub._handlers)
    self.assertFalse(INTENT_TOPIC % 'intent2' in skill._pubsub._handlers)

  def test_publications(self):
    data = { 'intents': { 'something': None, 'somethingElse': None } }

    pb = PubSub()
    pb.publish = MagicMock()

    skill = SkillAdapter(pb)
    skill.attach(data)

    skill.register()

    pb.publish.assert_called_once_with(ATLAS_REGISTRY_SKILL, '{"intents": {"something": null, "somethingElse": null}}')
    pb.publish.reset_mock()

    skill.end({})

    pb.publish.assert_called_once_with(DIALOG_END_TOPIC, "{}")
    pb.publish.reset_mock()

    skill.answer({ 'text': 'Hello you!' })
    pb.publish.assert_called_once_with(DIALOG_ANSWER_TOPIC, '{"text": "Hello you!"}')
    pb.publish.reset_mock()

    skill.ask({ 'slot': 'location' })
    pb.publish.assert_called_once_with(DIALOG_ASK_TOPIC, '{"slot": "location"}')
    pb.publish.reset_mock()