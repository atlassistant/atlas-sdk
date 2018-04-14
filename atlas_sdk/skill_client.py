from .client import Client, INTENT_TOPIC
from .request import Request
from .broker import BrokerConfig
from .version import __version__
import logging, argparse, sys

class SkillClient(Client):
  """Main class when you want to describe and register an Atlas skill.

  """
  
  def __init__(self, name, version, description=None, intents=[], env=[]):
    """Initialize a new Skill.

    :param name: Name of the skill
    :type name: str
    :param version: Version of the skill
    :type version: str
    :param description: Optional description of the skill
    :type description: str
    :param intents: List of intents supported by this skill
    :type intents: list
    :param env: List of configuration variables needed by this skill
    :type env: list
    """

    super(SkillClient, self).__init__(name='sdk')

    # TODO make a skill class shared between the sdk and the core

    self.name = name
    self.version = version
    self.description = description
    self.intents = intents
    self.env = env

    self.log.info('Created skill %s\n\t%s' % (self, '\n\t'.join([s.__str__() for s in self.env])))

  def __str__(self):
    return '%s %s - %s' % (self.name, self.version, self.description or 'No description')

  def on_connect(self, client, userdata, flags, rc):
    super(SkillClient, self).on_connect(client, userdata, flags, rc)

    for intent in self.intents:
      topic = INTENT_TOPIC % intent.name
      self.subscribe_json(topic, lambda d, r: intent.handler(Request(d, r)))
      self.log.info('Subscribed to topic %s' % topic)

  def run(self):
    """Parses current os args and run the MQTT loop.
    """

    parser = argparse.ArgumentParser(description='Atlas SDK %s' % __version__)

    parser.add_argument('-H', '--host', help='MQTT host address')
    parser.add_argument('-p', '--port', help='MQTT port')
    parser.add_argument('-u', '--user', help='Username and password for the mqtt in the form user:password')

    args = parser.parse_args(sys.argv[1:])

    # TODO yeah I know that's a bit ugly

    user, pwd = (args.user or ':').split(':')

    args_dict = {
      'host': args.host,
      'port': args.port,
      'username': user,
      'password': pwd,
    }
    
    self.start(BrokerConfig(**{ k: v for k,v in args_dict.items() if v != None }), False)