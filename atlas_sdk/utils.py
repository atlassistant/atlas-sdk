import random

def choose_one(choices):
  """Choose a random element in the given list. If `choices` is not a list, it will
  be returned.

  Args:
    choices (obj, list): List or object
  """

  if type(choices) is not list:
    return choices

  return random.choice(choices)

def create_instance_of(qualified_name, **kwargs):
  """Creates an instance of the fully qualified name of a class.

  Args:
    qualified_name (str): Full name of the class to instantiate
    kwargs: Other arguments that will be forwarded

  Returns:
    obj: Instance of the asked class

  """

  parts = qualified_name.split('.')
  klass = parts[-1:][0]
  mod = __import__('.'.join(parts[:-1]), fromlist=[klass])

  return getattr(mod, klass)(**kwargs)