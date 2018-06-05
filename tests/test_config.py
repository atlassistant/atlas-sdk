import unittest
from unittest import mock
from atlas_sdk.config import Config, load_from_yaml, config

class ConfigTests(unittest.TestCase):

  @mock.patch('builtins.open')
  def test_load_from_yaml(self, mock_open):
    mock_open.side_effect = [
      mock.mock_open(read_data='''
broker:
  host: localhost
  port: 1883
database:
  host: localhost
  name: My DB
''').return_value
    ]

    load_from_yaml('config.yml')

    self.assertIsNotNone(config)
    self.assertEqual('localhost', config.get('broker.host'))
    self.assertEqual(1883, config.get('broker.port'))
    self.assertEqual('localhost', config.get('database.host'))
    self.assertEqual('My DB', config.get('database.name'))

  def test_empty_config(self):
    c = Config()

    self.assertIsNone(c.get('broker.host'))

  def test_partial_config(self):
    c = Config({
      'broker': {
        'host': 'localhost',
        'port': 1883,
      },
    })

    self.assertEqual('localhost', c.get('broker.host'))
    self.assertEqual(1883, c.get('broker.port'))
    self.assertIsNone(c.get('broker.something'))

  def test_get_with_remove_keys(self):
    data = {
      'broker': {
        'host': 'localhost',
        'port': 1883,
      },
    }
    c = Config(data)

    result = c.get('broker', keys_to_remove=['port', 'not_in_config'])

    self.assertEqual({ 'host': 'localhost' }, result)
    self.assertEqual(data, dict(c)) # Check if has not been modified

  def test_default(self):
    c = Config()

    self.assertEqual('something', c.get('doesntexist', 'something'))
