import logging
from datetime import datetime
from dateutil.parser import parse as dateParse
from .adapters import ChannelAdapter
from .pubsubs import PubSub
from .constants import STARTED_AT_KEY, LANG_KEY

class Channel:
  """A channel is single source of communication with the server.

    It is created for a particular user. It can be anything you want, a terminal,
    a voice input, a web app.

    You can pass your own handlers by using the constructor or subclass it and make your
    own channel.

    This class already handle channel recreate if the server has been restarted by attaching to the
    `on_discovery_ping` handler.
  """

  def __init__(self, id, user_id=None, adapter=None, 
    on_created=None, on_destroyed=None, on_answer=None, on_ask=None, on_end=None, on_work=None):
    """Creates a new channel.

    Args:
      id (str): ID of the channel, it should be unique per channel and per user
      user_id (str): User identifier
      adapter (ChannelAdapter): Adapter to use, if no one is given, a default one will be created
      on_created (callable): Called when the channel has been created by the server
      on_destroyed (callable): Called when the channel has been destroyed by the server
      on_answer (callable): Called when the skill wants to answer to the user
      on_ask (callable): Called when the skill asks for user input
      on_end (callable): Called when a session has ended
      on_work (callable): Called when a skill is working

    """

    self._logger = logging.getLogger(self.__class__.__name__)
    self._created_at = None
    self._lang = None
    self._adapter = adapter or ChannelAdapter(PubSub.from_config())
    self._adapter.attach(id, user_id)

    self._adapter.on_discovery_ping = self.check_still_connected
    self._adapter.on_created = self.on_created

    self._adapter.on_answer =     on_answer or self._adapter.on_answer
    self._adapter.on_ask =        on_ask or self._adapter.on_ask
    self._adapter.on_destroyed =  on_destroyed or self._adapter.on_destroyed
    self._adapter.on_end =        on_end or self._adapter.on_end
    self._adapter.on_work =       on_work or self._adapter.on_work

    self._on_created = on_created

  def lang(self):
    """Gets the channel language.

    Returns:
      str: Language of the channel

    """

    return self._lang

  def parse(self, msg):
    """Parses a message.

    Args:
      msg (str): Message to parse.

    """

    self._adapter.parse(msg)

  def on_created(self, data):
    """Called when the channel has been created and an agent is ready.

    Args:
      data (dict): Data sent by the server
    
    """

    self._created_at = datetime.utcnow()
    self._lang = data.get(LANG_KEY)
    
    self._logger.debug('Channel created at %s for lang %s' % (self._created_at, self._lang))

    if self._on_created:
      self._on_created(data)

  def check_still_connected(self, data):
    """Upon discovery ping, checks if the channel is still connected to prevent
    error when atlas has been down.

    Args:
      data (dict): Data sent by the server
    
    """

    start_date_str = data.get(STARTED_AT_KEY)

    if start_date_str:
      start_date = dateParse(start_date_str)

      if start_date > self._created_at:
        self._logger.info('Recreating the channel, looks like the server has been restarted')
        self._adapter.create()

  def run(self):
    """Launch this channel, activate the underlying adapter.
    """

    self._adapter.activate()

  def cleanup(self):
    """Cleanup this channel, deactivate the adapter.
    """

    self._adapter.deactivate()