from json import dumps
from ..pubsubs.handlers import json, notset, empty
from .pubsub_adapter import PubSubAdapter
from ..pubsubs.constants import ON_CONNECTED_TOPIC
from ..topics import INTENT_TOPIC, DISCOVERY_PING_TOPIC, DISCOVERY_PONG_TOPIC, \
  DIALOG_ANSWER_TOPIC, DIALOG_ASK_TOPIC, DIALOG_END_TOPIC
from ..constants import INTENTS_KEY

class SkillAdapter(PubSubAdapter):
  
  def __init__(self, pubsub):
    """Constructs a new skill adapter.

    You must call `attach` with the skill data to make discovery answer work as expected.

    Args:
      pubsub (PubSub): PubSub implementation to use

    """

    super(SkillAdapter, self).__init__(pubsub)

    self._skill_data = {
      INTENTS_KEY: {},
    }

    self.on_discovery_ping = notset(self._logger)

    self._on_discovery_handler = None
    self._on_connected_handler = None

  def attach(self, skill_data):
    """Attach skill data to this adapter. Used by the pong method.

    Args:
      skill_data (dict): Dictionary representing the skill, used for discovery purposes

    """

    self._skill_data = skill_data

  def handle(self, intent, handler):
    """Subscribe for a given intent.

    Args:
      intent (str): Intent name to handle
      handler (callable): Handler to call

    """

    if intent not in self._skill_data.get(INTENTS_KEY, {}):
      self._logger.warning('Subscribing to "%s", which is not part of the skill metadata! Added it' % intent)
      self._skill_data.get(INTENTS_KEY, {})[intent] = None

    self._pubsub.subscribe(intent, json(handler))

  def pong(self):
    """Sends a pong discovery answer.
    """

    self._pubsub.publish(DISCOVERY_PONG_TOPIC, dumps(self._skill_data))

  def ask(self, data):
    """Ask something to the user.

    Args:
      data (dict): Data to send with the request
      
    """

    self._pubsub.publish(DIALOG_ASK_TOPIC, dumps(data))

  def answer(self, data):
    """Answer something to the user.

    Args:
      data (dict): Data to send with the request

    """

    self._pubsub.publish(DIALOG_ANSWER_TOPIC, dumps(data))

  def end(self, data):
    """Ends a conversation with the user.

    Args:
      data (dict): Data to send with the request

    """
    
    self._pubsub.publish(DIALOG_END_TOPIC, dumps(data))

  def activate(self):
    self._on_connected_handler = empty(self.pong)
    self._on_discovery_handler = json(self.on_discovery_ping)

    self._pubsub.subscribe(ON_CONNECTED_TOPIC,      self._on_connected_handler)
    self._pubsub.subscribe(DISCOVERY_PING_TOPIC ,   self._on_discovery_handler)

    super(SkillAdapter, self).activate()

  def deactivate(self):
    self._pubsub.unsubscribe(ON_CONNECTED_TOPIC,    self._on_connected_handler)
    self._pubsub.unsubscribe(DISCOVERY_PING_TOPIC,  self._on_discovery_handler)

    # Unsubscribe properly to each metadata skills
    for intent in self._skill_data.get(INTENTS_KEY, {}).keys():
      self._pubsub.unsubscribe(intent)

    super(SkillAdapter, self).deactivate()