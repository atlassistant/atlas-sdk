from .facade import Facade

class PubSubFacade(Facade):
  """Represents a facade that uses a PubSub instance to communicate with the
  outside world.

  Basically, you subclass this class, defines methods which handle publications and
  make available some callback (self.on_your_event).

  Users of this class should create an instance, register their own callbacks with 
  `facade.on_your_event = self.my_handler` and call `activate` to effectively subscribe
  to appropriate topics.

  Examples:
    >>> facade = PubSubFacadeSubclass(publisher_implementation)
    >>> facade.on_an_event = your_handler
    >>> facade.activate()

  """

  def __init__(self, pubsub):
    """Constructs a new PubSubFacade.

    Args:
      pubsub (PubSub): PubSub implementation to use

    """
    
    super(PubSubFacade, self).__init__()

    self._pubsub = pubsub

  def activate(self):
    super(PubSubFacade, self).activate()

    self._pubsub.start()

  def deactivate(self):
    super(PubSubFacade, self).deactivate()

    self._pubsub.stop()