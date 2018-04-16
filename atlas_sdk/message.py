class Message():
  """Represents an MQTT message with handy function baked in.
  """

  def __init__(self, data, raw):
    """Constructs a new message from an incoming message.

    :param data: Json data of the message
    :type data: dict
    :param raw: Raw message
    :type raw: str
    """

    self.data = data
    self.raw = raw

    # Extract common properties

    self.id = data.get('__id')
    self.uid = data.get('__uid')
    self.lang = data.get('__lang')
    self.atlas_version = data.get('__version')

  def env(self, key):
    """Retrieve a configuration key for this message.

    :param key: Key to retrieve
    :type key: str

    """

    return self.data.get('__env', {}).get(key)

  def slot(self, name, default=None):
    """Handy method to retrieve a slot value for this message.

    :param name: Slot name to retrieve
    :type name: str
    :param default: Default value if not found
    :type default: any
    
    """

    return self.data.get(name, default)
