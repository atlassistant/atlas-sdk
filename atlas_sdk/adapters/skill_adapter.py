from json import dumps
from ..pubsubs.handlers import json
from .pubsub_adapter import PubSubAdapter
from ..topics import INTENT_TOPIC, DISCOVERY_PING_TOPIC, DISCOVERY_PONG_TOPIC

class SkillAdapter(PubSubAdapter):
  
  def __init__(self, pubsub, skill_data):
    """Constructs a new skill adapter.

    Args:
      pubsub (PubSub): PubSub implementation to use
      skill_data (dict): Dictionary representing the skill, used for discovery purposes

    """

    super(SkillAdapter, self).__init__(pubsub)

    self._skill_data = skill_data

  def pong(self):
    """Sends a pong discovery answer.
    """

    self._pubsub.publish(DISCOVERY_PONG_TOPIC, dumps(self._skill_data))

  def _on_discovery_request(self, data):
    """Called when a discovery request has been send by the service.

    Args:
      data (dict): Data sent by the service
    
    """

    self.pong()

  def activate(self):
    self._pubsub.subscribe(DISCOVERY_PING_TOPIC , json(self._on_discovery_request))

    super(SkillAdapter, self).activate()