import unittest
from unittest.mock import patch, mock_open
from atlas_sdk import Skill

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