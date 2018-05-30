class AttrDict(dict):
  """Tiny readonly wrapper around a dict to provide attribute like access.
  """

  def __getitem__(self, key):
    value = dict.__getitem__(self, key)
    return AttrDict(value) if isinstance(value, dict) else value

  __getattr__ = __getitem__

  @classmethod
  def empty(cls):
    return AttrDict({ 'value': None })

class SlotData():
  """Represents slot data and exposes some utility methods.
  """

  def __init__(self, data=None):
    """Constructs a new slot data from raw slot values.

    :param data: Raw slot values
    :type data: list

    """

    self.data = data or []

  def __getitem__(self, x):
    """Retrieve an element at the given index.

    :rtype: AttrDict

    """
    return AttrDict(self.data[x])

  def __len__(self):
    return len(self.data)

  def first(self):
    """Retrieve the first value of a slot.

    If there is no value, an empty AttrDict will be returned.

    :rtype: AttrDict

    """

    return AttrDict(self.data[0]) if len(self.data) > 0 else AttrDict.empty()

  def last(self):
    """Retrieve the last value of a slot.

    If there is no value, an empty AttrDict will be returned.
    
    :rtype: AttrDict

    """

    return AttrDict(self.data[len(self.data) - 1]) if len(self.data) > 0 else AttrDict.empty()