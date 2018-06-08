import unittest, types
from unittest.mock import patch, mock_open, MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.adapters import SkillAdapter
from atlas_sdk import Skill
from atlas_sdk import Request
from atlas_sdk.topics import INTENT_TOPIC

class SkillTests(unittest.TestCase):
  
  @patch('builtins.open')
  def test_from_config(self, m_open):
    m_open.side_effect = [
      mock_open(read_data='''
skill:
  name: TestSkill
  version: 1.0.0
  author: Julien LEICHER
  intents:
    showSomething:
      - slotValue1
      - slotValue2
    showSomethingElse:
  settings:
    - server.url
messaging:
  host: 127.0.0.1
''').return_value
    ]

    skill = Skill.from_config('conf.yml')

    self.assertEqual('TestSkill', skill.name)
    self.assertEqual('1.0.0', skill.version)
    self.assertEqual('Julien LEICHER', skill.author)
    self.assertEqual('127.0.0.1', skill._adapter._pubsub._host)
    self.assertTrue('showSomething' in skill.intents)
    self.assertEqual(['slotValue1', 'slotValue2'], skill.intents['showSomething'])
    self.assertTrue('showSomethingElse' in skill.intents)
    self.assertEqual(['server.url'], skill.settings)

  def test_translations(self):
    self.skipTest('Find a way to mock it')

  def test_handlers(self):
    obj = types.SimpleNamespace()
    obj.handler1 = MagicMock()
    obj.handler2 = MagicMock()
    obj.on_atlas_loaded = MagicMock()
    obj.on_atlas_unloaded = MagicMock()

    pb = PubSub()
    adapter = SkillAdapter(pb)
    skill = Skill(name='test skill', version='1.0.0', adapter=adapter,
      on_atlas_loaded=obj.on_atlas_loaded,
      on_atlas_unloaded=obj.on_atlas_unloaded)
      
    skill._install_translation = MagicMock()

    skill.handle('intent1', obj.handler1)
    skill.handle('intent2', obj.handler2)

    pb.on_received(INTENT_TOPIC % 'intent1', '{"__lang": "fr"}')
    skill._install_translation.assert_called_once_with('fr')

    obj.handler1.assert_called_once()
    obj.handler2.assert_not_called()

    skill._install_translation.reset_mock()
    obj.handler1.reset_mock()
    obj.handler2.reset_mock()
    
    pb.on_received(INTENT_TOPIC % 'intent2', '{"__lang": "en"}')
    skill._install_translation.assert_called_once_with('en')
    obj.handler1.assert_not_called()
    obj.handler2.assert_called_once()

    adapter.on_atlas_loaded({})
    adapter.on_atlas_unloaded()
    obj.on_atlas_loaded.assert_called_once_with({})
    obj.on_atlas_unloaded.assert_called_once_with()