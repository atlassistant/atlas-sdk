import logging
from .runnable import Runnable
from .adapters import ChannelAdapter
from .pubsubs import PubSub
from .config import load_from_yaml, config

class Channel(Runnable):
  """A channel is single source of communication with the server.

    It is created for a particular user. It can be anything you want, a terminal,
    a voice input, a web app.

    You can pass your own handlers by using the constructor or subclass it and make your
    own channel.

    This class already handle channel recreate if the server has been restarted by attaching to the
    `on_discovery_ping` handler.
  """

  def __init__(self, id, user_id=None, adapter=None, 
    on_created=None, on_destroyed=None, on_answer=None, on_ask=None, on_end=None, on_work=None,
    on_atlas_loaded=None, on_atlas_unloaded=None):
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
      on_atlas_loaded (callable): Called when atlas server has been loaded
      on_atlas_unloaded (callable): Called when atlas server has been unloaded

    """

    self._logger = logging.getLogger(self.__class__.__name__)
    self._adapter = adapter or ChannelAdapter(PubSub.from_config())
    self._adapter.attach(id, user_id)

    self._adapter.on_answer =         on_answer or self._adapter.on_answer
    self._adapter.on_ask =            on_ask or self._adapter.on_ask
    self._adapter.on_created =        on_created or self._adapter.on_created
    self._adapter.on_destroyed =      on_destroyed or self._adapter.on_destroyed
    self._adapter.on_end =            on_end or self._adapter.on_end
    self._adapter.on_work =           on_work or self._adapter.on_work
    self._adapter.on_atlas_loaded =   on_atlas_loaded or self._adapter.on_atlas_loaded
    self._adapter.on_atlas_unloaded = on_atlas_unloaded or self._adapter.on_atlas_unloaded

  def parse(self, msg):
    """Parses a message.

    Args:
      msg (str): Message to parse.

    """

    self._adapter.parse(msg)

  def run(self):
    self._adapter.activate()

  def cleanup(self):
    self._adapter.deactivate()

  @classmethod
  def from_config(cls, path):
    """Instantiates a new channel based on the configuration file given.

    Args:
      path (str): Path to the configuration file
    Returns:
      Channel: A channel instance

    """

    load_from_yaml(path)

    return Channel(**config.get('channel', {}))