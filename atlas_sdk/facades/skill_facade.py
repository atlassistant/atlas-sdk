from .pubsub_facade import PubSubFacade
from .topics import INTENT_TOPIC, DISCOVERY_PING_TOPIC, DISCOVERY_PONG_TOPIC

class SkillFacade(PubSubFacade):
  
  def __init__(self, pubsub):
    super(SkillFacade, self).__init__(pubsub)

  def pong(self):
    pass