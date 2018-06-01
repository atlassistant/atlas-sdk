import sys
from .pubsub import PubSub
from .constants import lifecycle_topics, ON_CONNECTED_TOPIC, ON_DISCONNECTED_TOPIC
from paho.mqtt.client import Client

class MQTTPubSub(PubSub):
  """Publisher / Subscriber implemented with MQTT
  """

  def __init__(self, client_id=None, host='localhost', port=1883, user=None, password=None, threaded=True):
    """Instantiates a new MQTT client with the given configuration.

    Args:
      client_id (str): Client ID used by the broker to identify the session
      host (str): Broker host
      port (int): Broker port
      user (str): Username if using authentication
      password (str): Password if using authentication
      threaded (bool): Boolean to determine if this client lives in its own thread

    """
    
    super(MQTTPubSub, self).__init__()

    self._started_count = 0

    self._client = Client(client_id)
    self._client.on_connect = self._on_connect
    self._client.on_disconnect = self._on_disconnect
    self._client.on_message = self._on_message

    self._host = host
    self._port = port
    self._user = user
    self._password = password
    self._threaded = threaded

  def _on_connect(self, client, userdata, flags, rc):
    self._is_started = True
    self._logger.info('✔️ Connected to broker')

    # Subscribe to each topic registered
    for topic in self._handlers.keys():
      if topic not in lifecycle_topics:
        self._client.subscribe(topic)

    self.publish(ON_CONNECTED_TOPIC)

  def _on_disconnect(self, client, userdata, rc):
    self._is_started = False
    self._logger.info('❌ Disconnected')

    self.publish(ON_DISCONNECTED_TOPIC)

  def _on_message(self, client, userdata, msg):
    self.on_received(msg.topic, msg.payload)

  def publish(self, topic, payload=None):
    self._logger.debug('Publishing to %s with payload %s' % (topic, payload))

    if topic in lifecycle_topics:
      self.on_received(topic, payload)
    else:
      self._client.publish(topic, payload, qos=1)

  def subscribe(self, topic, handler):
    super(MQTTPubSub, self).subscribe(topic, handler)

    # If already started, just subscribe immediately
    if self.is_started() and topic not in lifecycle_topics:
      self._client.subscribe(topic)

  def unsubscribe(self, topic):
    super(MQTTPubSub, self).unsubscribe(topic)
    
    self._client.unsubscribe(topic)

  def start(self):
    self._started_count += 1

    if self._started_count > 1:
      # If it has been already connected, just publish the on connected callback
      
      # TODO it may be tricky when sharing the pubsub on multiple adapters, wait & see but for the
      # on connected topic, action are not destructive so that's not a big deal I guess
      return self.publish(ON_CONNECTED_TOPIC)
      
    if self._user:
        self._client.username_pw_set(self._user, self._password)

    try:
      self._client.connect(self._host, self._port)

      if self._threaded:
        self._client.loop_start()
      else:
        try:
          self._client.loop_forever()
        except KeyboardInterrupt:
          pass
    except ConnectionRefusedError as e:
      self._started_count -= 1
      self._logger.critical('Could not connect to the broker at %s:%s, is it running?' % (self._host, self._port))
      sys.exit(-1)

  def stop(self):
    if self._started_count > 1:
      # More than one client still using it, just decrement the count
      self._started_count -= 1

      # TODO maybe we should send the on disconnected topic here, but it's so tricky on multiple adapters...
    else:
      self._client.loop_stop()
      self._client.disconnect()