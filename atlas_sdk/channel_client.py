from .client import Client, \
  CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC, CHANNEL_ASK_TOPIC, CHANNEL_SHOW_TOPIC, \
  CHANNEL_TERMINATE_TOPIC, DIALOG_PARSE_TOPIC, CHANNEL_WORK_TOPIC, DISCOVERY_PING_TOPIC, \
  CHANNEL_CREATED_TOPIC, CHANNEL_DESTROYED_TOPIC
import json
from datetime import datetime
from dateutil.parser import parse

class ChannelClient(Client):
  """A channel client should be used by end client only. It leverages messages used by a channel.

  It represents connections with the broker that provides user inputs, wether it's voice, text or whatever. It is instantiated
  on a per user basis.

  """
    
  def __init__(self, client_id, user_id, on_ask=None, on_show=None, on_terminate=None, on_work=None, on_created=None, on_destroyed=None):
    """Constructs a new ChannelClient.
    
    :param client_id: Client ID to use, it's commonly a session id
    :type client_id: str
    :param user_id: User ID attached to this channel
    :type user_id: str
    :param on_ask: Handler when the dialog engine wants the channel to ask something
    :type on_ask: callable
    :param on_show: Handler when the dialog engine wants the channel to show something
    :type on_show: callable
    :param on_terminate: Handler when the dialog engine wants the channel to terminate the dialog
    :type on_terminate: callable
    :param on_work: Handler when the dialog engine wants to inform the channel that a work has been started
    :type on_work: callable
    :param on_created: Handler when the channel has been successfuly created by atlas
    :type on_created: callable
    :param on_destroyed: Handler when the channel has been destroyed by atlas
    :type on_destroyed: callable

    """

    super(ChannelClient, self).__init__(client_id, 'channel.' + client_id)

    self.CHANNEL_CREATE_TOPIC = CHANNEL_CREATE_TOPIC % client_id
    self.CHANNEL_CREATED_TOPIC = CHANNEL_CREATED_TOPIC % client_id
    self.CHANNEL_DESTROY_TOPIC = CHANNEL_DESTROY_TOPIC % client_id
    self.CHANNEL_DESTROYED_TOPIC = CHANNEL_DESTROYED_TOPIC % client_id
    self.CHANNEL_ASK_TOPIC = CHANNEL_ASK_TOPIC % client_id
    self.CHANNEL_SHOW_TOPIC = CHANNEL_SHOW_TOPIC % client_id
    self.CHANNEL_TERMINATE_TOPIC = CHANNEL_TERMINATE_TOPIC % client_id
    self.CHANNEL_WORK_TOPIC = CHANNEL_WORK_TOPIC % client_id
    self.DIALOG_PARSE_TOPIC = DIALOG_PARSE_TOPIC % client_id

    self.on_ask = on_ask or self.handler_not_set
    self.on_show = on_show or self.handler_not_set
    self.on_terminate = on_terminate or self.handler_not_set
    self.on_work = on_work or self.handler_not_set
    self.on_destroyed = on_destroyed or self.handler_not_set
    self.on_created = on_created or self.handler_not_set

    self.uid = user_id
    self._created_at = None

  def on_connect(self, client, userdata, flags, rc):
    super(ChannelClient, self).on_connect(client, userdata, flags, rc)

    self.subscribe_json(self.CHANNEL_ASK_TOPIC, self.on_ask)
    self.subscribe_json(self.CHANNEL_SHOW_TOPIC, self.on_show)
    self.subscribe_json(DISCOVERY_PING_TOPIC, self._check_still_connected)
    self.subscribe_void(self.CHANNEL_TERMINATE_TOPIC, self.on_terminate)
    self.subscribe_void(self.CHANNEL_WORK_TOPIC, self.on_work)
    self.subscribe_void(self.CHANNEL_DESTROYED_TOPIC, self.on_destroyed)
    self.subscribe_json(self.CHANNEL_CREATED_TOPIC, self.on_created)

    self.create()

  def _check_still_connected(self, data, raw):
    """Checks if the channel is still connected to the client and if its not, reconnects it.

    :param data: JSON data received
    :type data: dict
    :param raw: Raw payload
    :type raw: str

    """

    start_date_str = data.get('started_at')

    if start_date_str:
      start_date = parse(start_date_str)

      if start_date > self._created_at:
        self.log.info('Recreating the channel, looks like the server has been restarted')
        self.create()

  def stop(self):
    self.destroy()

    super(ChannelClient, self).stop()

  def create(self):
    """Inform the atlas engine of the channel creation.

    This is used by atlas to provide an agent for this channel.
    """

    self._created_at = datetime.utcnow()
        
    self.publish(self.CHANNEL_CREATE_TOPIC, json.dumps({ 'uid': self.uid }))

  def destroy(self):
    """Inform the atlas engine that this channel is going down.
    """

    self.publish(self.CHANNEL_DESTROY_TOPIC)

  def parse(self, msg):
    """Ask the dialog engine to parse the given message.

    :param msg: Message to parse
    :type msg: str

    """

    self.publish(self.DIALOG_PARSE_TOPIC, msg)