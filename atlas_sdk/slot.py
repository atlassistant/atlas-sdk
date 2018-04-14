class Slot():
  """Represents a single intent slot (ie. a parameter).
  """

  def __init__(self, name):
    """Constructs a new slot.

    :param name: Name of the slot
    :type name: str

    """

    self.name = name
  
  def __str__(self):
    return 'Slot %s' % self.name