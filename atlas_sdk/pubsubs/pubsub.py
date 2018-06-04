import logging
from ..utils import create_instance_of
from ..config import config

class PubSub:
  """Publisher / Subscriber basic class.

  It exposes methods for publishing / subscribing to topics without defining
  the underlying method so you must subclass it to implement the publish`

  It makes replacing the standard MQTT behavior much easy.

  """

  def __init__(self):
    """Constructs a new empty PubSub instance.
    """

    self._handlers = {}
    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._is_started = False

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, type, value, traceback):
    self.stop()

  def is_started(self):
    """Checks if this PubSub interface has been started.

    Returns:
      bool: Wether or not it has been started

    """

    return self._is_started

  def publish(self, topic, payload=None):
    """Publish a message to the given topic.

    Args:
      topic (str): Event to be published
      payload (obj): Any data to be sent with the event
    
    """

    self._logger.debug('Publishing to %s with payload %s' % (topic, payload))

    self.on_received(topic, payload)

  def on_received(self, topic, payload=None):
    """Method called when an event has been received by this PubSub instance.

    Args:
      topic (str): Topic received
      payload (obj): Data received
    
    """

    self._logger.debug('Received %s with payload %s' % (topic, payload))

    handlers = self._handlers.get(topic)

    if handlers:
      for handler in handlers:
        handler(topic, payload)
    else:
      self._logger.debug('No handler found for %s' % topic)

  def subscribe(self, topic, handler):
    """Subscribes to a given topic with the given handler.

    Args:
      topic (str): Topic to subscribe to
      handler (callable): Handler to be called on event, it will receive the topic and the message data

    """

    self._logger.debug('Subscribing to %s with %s' % (topic, handler))

    handlers = self._handlers.get(topic)

    if not handlers:
      self._handlers[topic] = [handler]
    else:
      handlers.append(handler)

  def unsubscribe(self, topic, handler=None):
    """Unsubscribes all handlers from the given topic.

    Args:
      topic (str): Topic to unsubscribe
      handler (callable): Specific handler to remove

    """

    self._logger.debug('Unsubscribing from %s' % topic)

    if topic in self._handlers:
      if handler:
        self._handlers[topic].remove(handler)

        if len(self._handlers[topic]) == 0:
          del self._handlers[topic]
      else:
        del self._handlers[topic]
    else:
      self._logger.warning('Trying to unsubscribe from a non-existent topic %s' % topic)

  def start(self):
    """Marks this PubSub interface has started.
    """

    self._is_started = True

  def stop(self):
    """Marks this PubSub interface has stopped.
    """

    self._is_started = False

  @classmethod
  def from_config(cls):
    return create_instance_of(
      config.get('messaging.type', 'atlas_sdk.pubsubs.mqtt_pubsub.MQTTPubSub'), 
      **config.get('messaging', {}, ['type']))