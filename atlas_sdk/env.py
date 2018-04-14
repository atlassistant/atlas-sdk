class Env():
  """Represents a single configuration parameter needed by a skill to work
  as correctly.
  """

  def __init__(self, name, description=None, var_type=str):
    """Constructs a new env requirement.

    :param name: Name of the configuration parameter
    :type name: str
    :param description: Description of the parameter
    :type description: str
    :param var_type: Type of the parameter
    :type var_type: type
    """

    self.name = name
    self.description = description
    self.type = var_type

  def __str__(self):
    return 'Env parameter %s %s - %s' % (self.name, self.type, self.description or 'No description')