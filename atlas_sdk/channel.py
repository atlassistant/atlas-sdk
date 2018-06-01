import logging
from datetime import datetime
from dateutil.parser import parse as dateParse
from .adapters import ChannelAdapter
from .pubsubs import PubSub
from .keys import STARTED_AT_KEY, LANG_KEY

class Channel:
  """A channel is single source of communication with the server.

    It is created for a particular user. It can be anything you want, a terminal,
    a voice input, a web app.

    Just subclass this class and use the underlying ChannelAdapter to register your handlers.

    This class already handle channel recreate if the server has been restarted by attaching to the
    `on_discovery_ping` handler.
  """

  def __init__(self, id, user_id, adapter=None):
    """Creates a new channel.

    Args:
      id (str): ID of the channel, it should be unique per channel and per user
      user_id (str): User identifier
      adapter (ChannelAdapter): Adapter to use, if no one is given, a default one will be created

    """

    self._logger = logging.getLogger(self.__class__.__name__)
    self._created_at = None
    self._lang = None
    self._adapter = adapter or ChannelAdapter(PubSub.from_config())
    self._adapter.attach(id, user_id)

    self._adapter.on_discovery_ping = self.check_still_connected
    self._adapter.on_created = self.on_created

  def lang(self):
    """Gets the channel language.

    Returns:
      str: Language of the channel

    """

    return self._lang

  def on_created(self, data):
    """Called when the channel has been created and an agent is ready.

    Args:
      data (dict): Data sent by the server
    
    """

    self._created_at = datetime.utcnow()
    self._lang = data.get(LANG_KEY)
    
    self._logger.debug('Channel created at %s for lang %s' % (self._created_at, self._lang))

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