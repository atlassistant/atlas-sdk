from .pubsubs import PubSub
from .runnable import Runnable
from .adapters import SkillAdapter
from .config import load_from_yaml, config
from .constants import NAME_KEY, DESCRIPTION_KEY, VERSION_KEY, AUTHOR_KEY, INTENTS_KEY

class Skill(Runnable):
  """A skill executes action based on intents parsed by the NLU.

  You must register your skill to specific intents and your handlers will be called by
  atlas when the intent has been recognized. Atlas will send you each slot that it
  will extract and start a conversation for your skill to ask for whatever it needs
  to accomplish its work.
  
  """

  def __init__(self, name, version, description=None, author=None, intents={}, adapter=None):
    """Initialize a new skill.

    Args:
      name (str): Name of the skill
      version (str): Version of the skill
      description (str): Optional description
      author (str): Optional author
      intents (dict): Dictionary of intents managed by your skill with associated slots
      adapter (SkillAdapter): Adapter to use to communicate with the outside world

    """

    self.name = name
    self.version = version
    self.author = author
    self.description = description
    self.intents = intents

    self._adapter = adapter or SkillAdapter(PubSub.from_config())
    self._adapter.attach({
      NAME_KEY: self.name,
      VERSION_KEY: self.version,
      AUTHOR_KEY: self.author,
      DESCRIPTION_KEY: self.description,
      INTENTS_KEY: self.intents,
    })

    self._adapter.on_discovery_ping = self.send_discovery_request

  def add_intent_handler(self, intent_name, handler):
    # self._adapter.subscribe()
    pass

  def send_discovery_request(self, data):
    """Sends a discovery request.

    Args:
      data (dict): Data sent by the service

    """

    self._adapter.pong()

  def run(self):
    self._adapter.activate()

  def cleanup(self):
    self._adapter.deactivate()

  @classmethod
  def from_config(cls, path):
    """Instantiates a new skill based on the configuration file given.

    Args:
      path (str): Path to the configuration file
    Returns:
      Skill: A skill instance

    """

    load_from_yaml(path)

    return Skill(**config.get('skill', {}))