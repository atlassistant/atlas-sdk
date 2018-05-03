"""This file contains all topics available for atlas for convenience since the SDK
is also used by atlas core itself.
"""

from .broker import BrokerConfig
import paho.mqtt.client as mqtt
import logging, json

# Discovery related topics

DISCOVERY_PING_TOPIC = 'atlas/discovery/ping'
DISCOVERY_PONG_TOPIC = 'atlas/discovery/pong'

# Dialog related topics, communication with an agent

DIALOG_TERMINATE_TOPIC = 'atlas/%s/dialog/terminate'
DIALOG_PARSE_TOPIC = 'atlas/%s/dialog/parse'
DIALOG_ASK_TOPIC = 'atlas/%s/dialog/ask'
DIALOG_SHOW_TOPIC = 'atlas/%s/dialog/show'

# Topic where request would be made available

INTENT_TOPIC = 'atlas/intents/%s'

# Channel related topics

CHANNEL_ASK_TOPIC = 'atlas/%s/channel/ask'
CHANNEL_SHOW_TOPIC = 'atlas/%s/channel/show'
CHANNEL_WORK_TOPIC = 'atlas/%s/channel/work'
CHANNEL_TERMINATE_TOPIC = 'atlas/%s/channel/terminate'
CHANNEL_CREATE_TOPIC = 'atlas/%s/channel/create'
CHANNEL_CREATED_TOPIC = 'atlas/%s/channel/created'
CHANNEL_DESTROY_TOPIC = 'atlas/%s/channel/destroy'
CHANNEL_DESTROYED_TOPIC = 'atlas/%s/channel/destroyed'

class Client:
  """Client is an helper class to handle messages management.
  """

  def __init__(self, client_id=None, name=None):
    """Constructs a new Client.

    :param client_id: Client ID to use when connecting
    :type client_id: str
    :param name: Name used by the logger
    :type name: str

    """

    self.log = logging.getLogger('atlas.client.%s' % (
      name or client_id or __class__.__name__))

    self._client = mqtt.Client(client_id)
    self._client.on_message = self.on_message
    self._client.on_connect = self.on_connect

    # Represents subscribed handlers for each type of subscriptions
    self._handlers = {
      'void': {},
      'raw': {},
      'json': {},
    }

  def handler_not_set(self, data=None, raw=None):
    self.log.warn('Handler not set correctly')

  def start(self, config, threaded=True):
    """Starts the broker client.

    :param config: Broker configuration
    :type config: BrokerConfig
    :param threaded: Wether or not it should run on its own thread
    :type threaded: bool

    """

    self._client.connect(config.host, config.port)

    if config.is_secured():
      self._client.username_pw_set(config.username, config.password)

    try:
      if threaded:
        self._client.loop_start()
      else:
        try:
          self._client.loop_forever()
        except KeyboardInterrupt:
          pass # Do nothing on keyboard interrupt
    except ConnectionRefusedError as e:
      self.log.critical('Could not connect to the MQTT: %s' % e.strerror)

  def stop(self):
    """Stops the broker client.
    """

    self._client.disconnect()
    self._client.loop_stop()

  def publish(self, topic, payload=None):
    """Publish a message to the given topic.

    You must transform the payload before calling this method.

    :param topic: Where to publish the message
    :type topic: str
    :param payload: Payload to publish
    :type payload: str

    """

    self._client.publish(topic, payload)

  def _subscribe(self, topic, ret, handler):
    """Inner subscribe which append the handler and subscribe to the topic.
    """

    # TODO May be we should use client.message_callback_add

    self._handlers[ret][topic] = handler
    self._client.subscribe(topic)
    self.log.debug('Subscribed to topic %s' % topic)

  def subscribe_json(self, topic, handler):
    """Subscribe to a topic with the given handler.

    Using this subscription type, the payload will be loaded via json and gave to the handler.

    For convenience, the handler should also take a second parameter which is the raw payload.

    :param topic: Topic to subscribe to
    :type topic: str
    :param handler: Handler to call
    :type handler: callable

    """

    self._subscribe(topic, 'json', handler)

  def subscribe_void(self, topic, handler):
    """Subscribe to a topic with the given handler.

    Using this subscription type, the payload will be empty.

    :param topic: Topic to subscribe to
    :type topic: str
    :param handler: Handler to call
    :type handler: callable

    """

    self._subscribe(topic, 'void', handler)

  def subscribe_raw(self, topic, handler):
    """Subscribe to a topic with the given handler.

    Using this subscription type, the payload will be send as it.

    :param topic: Topic to subscribe to
    :type topic: str
    :param handler: Handler to call
    :type handler: callable

    """

    self._subscribe(topic, 'raw', handler)

  def on_connect(self, client, userdata, flags, rc):
    self.log.info('✔️ Connected to broker')

  def on_disconnect(self, client, userdata, rc):
    self.log.info('❌ Disconnected')

  def on_message(self, client, userdata, msg):
    self.log.debug('Received message %s - %s' % (msg.topic, msg.payload))

    handler = self._handlers['raw'].get(msg.topic)

    if handler:
      handler(msg.payload.decode('utf-8'))
    else:
      handler = self._handlers['void'].get(msg.topic)

      if handler:
        handler()
      else:
        handler = self._handlers['json'].get(msg.topic)

        if handler:
          try:
            data = json.loads(msg.payload)
          except json.decoder.JSONDecodeError:
            data = {}
            self.log.warn('Could not decode payload %s' % msg.payload)

          handler(data, msg.payload)
        else:
            self.log.warn('No handler found for %s' % msg.topic)
