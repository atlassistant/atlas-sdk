from .adapter import Adapter

class PubSubAdapter(Adapter):
  """Represents an adapter that uses a PubSub instance to communicate with the
  outside world.

  Basically, you subclass this class, defines methods which handle publications and
  make available some callback (self.on_your_event).

  Users of this class should create an instance, register their own callbacks with 
  `adapter.on_your_event = self.my_handler` and call `activate` to effectively subscribe
  to appropriate topics.

  Examples:
    >>> adapter = PubSubAdapter(publisher_implementation)
    >>> adapter.on_an_event = your_handler
    >>> adapter.activate()

  """

  def __init__(self, pubsub):
    """Constructs a new PubSubAdapter.

    Args:
      pubsub (PubSub): PubSub implementation to use

    """
    
    super(PubSubAdapter, self).__init__()

    self._pubsub = pubsub

  def activate(self):
    super(PubSubAdapter, self).activate()

    self._pubsub.start()

  def deactivate(self):
    super(PubSubAdapter, self).deactivate()

    self._pubsub.stop()