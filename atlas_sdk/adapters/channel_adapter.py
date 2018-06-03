from json import dumps
from datetime import datetime
from .pubsub_adapter import PubSubAdapter
from ..pubsubs.constants import ON_CONNECTED_TOPIC
from ..pubsubs.handlers import json, empty, notset
from ..topics import CHANNEL_ANSWER_TOPIC, CHANNEL_ASK_TOPIC, CHANNEL_CREATE_TOPIC, \
  CHANNEL_CREATED_TOPIC, CHANNEL_DESTROY_TOPIC, CHANNEL_DESTROYED_TOPIC, CHANNEL_END_TOPIC, \
  CHANNEL_WORK_TOPIC, DIALOG_PARSE_TOPIC, DISCOVERY_PING_TOPIC
from ..constants import USER_ID_KEY

class ChannelAdapter(PubSubAdapter):

  def __init__(self, pubsub):
    """Constructs a new adapter for a Channel.

    You must call `attach` before the activation!

    Args:
      pubsub (PubSub): PubSub implementation to use

    """

    super(ChannelAdapter, self).__init__(pubsub)

    self._channel_id = None
    self._user_id = None

    # This is what should be exposed

    self.on_ask = notset(self._logger)
    self.on_answer = notset(self._logger)
    self.on_end = notset(self._logger)
    self.on_work = notset(self._logger)
    self.on_destroyed = notset(self._logger)
    self.on_created = notset(self._logger)
    self.on_discovery_ping = notset(self._logger)

    self._on_discovery_handler = None
    self._on_create_handler = None

  def attach(self, channel_id, user_id):
    """Attach this adapter to the given ids, it should be called before the activate!
    
    Args:
      channel_id (str): Channel unique id, used for topic naming
      user_id (obj): User id for this channel

    """

    self._channel_id = channel_id
    self._user_id = user_id

  def create(self):
    """Inform atlas that this channel has been created.
    """

    self._created_at = datetime.utcnow()

    self._pubsub.publish(CHANNEL_CREATE_TOPIC % self._channel_id, dumps({
      USER_ID_KEY: self._user_id
    }))

  def destroy(self):
    """Inform atlas that this channel has been destroyed. This will delete the 
    associated agent.
    """

    self._pubsub.publish(CHANNEL_DESTROY_TOPIC % self._channel_id)

  def parse(self, msg):
    """Sends a message to be parsed.

    Args:
      msg (str): Message to send

    """

    self._pubsub.publish(DIALOG_PARSE_TOPIC % self._channel_id, msg)

  def activate(self):
    self._on_create_handler = empty(self.create)
    self._on_discovery_handler = json(self.on_discovery_ping)

    self._pubsub.subscribe(ON_CONNECTED_TOPIC,                          self._on_create_handler)
    self._pubsub.subscribe(DISCOVERY_PING_TOPIC,                        self._on_discovery_handler)

    self._pubsub.subscribe(CHANNEL_ASK_TOPIC % self._channel_id,        json(self.on_ask))
    self._pubsub.subscribe(CHANNEL_ANSWER_TOPIC % self._channel_id,     json(self.on_answer))
    self._pubsub.subscribe(CHANNEL_END_TOPIC % self._channel_id,        empty(self.on_end))
    self._pubsub.subscribe(CHANNEL_WORK_TOPIC % self._channel_id,       empty(self.on_work))
    self._pubsub.subscribe(CHANNEL_DESTROYED_TOPIC % self._channel_id,  empty(self.on_destroyed))
    self._pubsub.subscribe(CHANNEL_CREATED_TOPIC % self._channel_id,    json(self.on_created))

    super(ChannelAdapter, self).activate()

  def deactivate(self, destroy=True):
    """Deactivate this facade.

    Args:
      destroy (bool): Wether or not a destroy request should be send to atlas

    """

    self._pubsub.unsubscribe(ON_CONNECTED_TOPIC, self._on_create_handler)
    self._pubsub.unsubscribe(DISCOVERY_PING_TOPIC, self._on_discovery_handler)

    self._pubsub.unsubscribe(CHANNEL_ASK_TOPIC % self._channel_id)
    self._pubsub.unsubscribe(CHANNEL_ANSWER_TOPIC % self._channel_id)
    self._pubsub.unsubscribe(CHANNEL_END_TOPIC % self._channel_id)
    self._pubsub.unsubscribe(CHANNEL_WORK_TOPIC % self._channel_id)
    self._pubsub.unsubscribe(CHANNEL_DESTROYED_TOPIC % self._channel_id)
    self._pubsub.unsubscribe(CHANNEL_CREATED_TOPIC % self._channel_id)

    if destroy:
      self.destroy()

    super(ChannelAdapter, self).deactivate()
