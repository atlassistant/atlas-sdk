class AttributeDict(dict):
  """Readonly dictionary with attribute like access.
  """

  def __getitem__(self, key):
    try:
      value = dict.__getitem__(self, key)
    except KeyError:
      return None

    return AttributeDict(value) if isinstance(value, dict) else value

  __getattr__ = __getitem__
  