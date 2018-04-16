class BrokerConfig:
  """Holds information about the broker connection.
  """

  def __init__(self, host='localhost', port=1883, username=None, password=None):
    """Constructs a new BrokerConfig.

    :param host: Broker host
    :type host: str
    :param port: Broker port
    :type port: int
    :param username: Optional broker username
    :type username: str
    :param password: Optional broker password
    :type password: str

    """

    self.host = host
    self.port = port
    self.username = username
    self.password = password

  def is_secured(self):
    """Checks if the broker configuration used credentials for the connection.

    :rtype: bool

    """

    return self.username and self.password

  def __str__(self):
    return '%s:%s@%s:%s' % (self.username, self.password, self.host, self.port)