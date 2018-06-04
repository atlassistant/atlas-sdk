from .pubsubs import PubSub
from .runnable import Runnable
from .adapters import SkillAdapter

class Skill(Runnable):
  """A skill executes action based on intents parsed by the NLU.

  You must register your skill to specific intents and your handlers will be called by
  atlas when the intent has been recognized. Atlas will send you each slot that it
  will extract and start a conversation for your skill to ask for whatever it needs
  to accomplish its work.
  
  """

  def __init__(self, name, version, description=None, author=None, adapter=None):
    """Initialize a new skill.
    """

    self._adapter = adapter or SkillAdapter(PubSub.from_config())

  def add_intent_handler(self, intent_name, handler):
    pass

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

    pass