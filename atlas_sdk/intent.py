class Intent():
  """Represents a single intent.
  """

  def __init__(self, name, handler, slots=[]):
    """Instantiates a new intent.

    :param name: Name of the intent
    :type name: str
    :param handler: Handler for this intent, it will receive a Message object with handy methods in it
    :type handler: callable
    :param slots: Slots needed by the skill for this intent
    :type slots: list

    """

    self.name = name
    self.handler = handler
    self.slots = slots

  def __str__(self):
    return 'Intent %s\n\t%s' % (self.name, '\n\t'.join([s.__str__() for s in self.slots]))