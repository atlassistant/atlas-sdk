import random
from semantic_version import Version, Spec
from .version import __version_requirements__

def validate_version(version):
  """Checks if the given version string validate the SDK requirements.

  Args:
    version (str): Version sent by the service

  Returns:
    bool: True if match, false otherwise
  
  """

  spec = Spec(__version_requirements__)

  return spec.match(Version(version))

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