from .attribute_dict import AttributeDict

class SlotData:
  """Represents slot data and exposes some utility methods.
  """

  def __init__(self, data=None):
    """Constructs a new slot data from raw slot values.

    Args:
      data (list): Slot available values

    """

    self.data = data or []

  def __getitem__(self, x):
    """Retrieve an element at the given index.
    
    Args:
      x (int): Index
    Returns:
      obj: Value

    """

    return AttributeDict(self.data[x])

  def __len__(self):
    return len(self.data)

  def is_empty(self):
    """Returns true if it does not have any value.

    Returns:
      bool: True if empty, false otherwise
    
    """
    return len(self.data) == 0

  def first(self):
    """Retrieve the first value of a slot.

    Returns:
      AttributeDict: An AttributeDict representing the first element

    """

    return AttributeDict(self.data[0]) if not self.is_empty() else AttributeDict()

  def last(self):
    """Retrieve the last value of a slot.

    Returns:
      AttributeDict: An AttributeDict representing the last element

    """

    return AttributeDict(self.data[len(self.data) - 1]) if not self.is_empty() else AttributeDict()
