class Request():
  """Represents an MQTT message with handy function baked in.
  """

  def __init__(self, data, raw):
    """Constructs a new request from an incoming message.
    """

    self.data = data
    self.raw = raw

  def ask(self):
    pass

  def show(self):
    pass

  def terminate(self):
    pass