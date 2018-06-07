import yaml, logging

class Config(dict):
  """Represents a global configuration object used in the entire system.

  It makes accessing configuration value a breeze with the .get() method.

  """
  
  def get(self, path, default=None, keys_to_remove=[]):
    """Retrieve configuration value for the given path.

    Args:
        path (str): Path with period for nested value
        default (obj): Default value if not found
        keys_to_remove (list): List of keys to remove if the return value is a dictionary
    Returns:
        obj: Value configurated or None if not found

    """

    cur_search_object = dict(self)

    for item in path.split('.'):
      cur_search_object = cur_search_object.get(item)

      if cur_search_object is None:
        return default

    if keys_to_remove and isinstance(cur_search_object, dict):
      cur_search_object = dict(cur_search_object) # Make a shallow copy

      for key in keys_to_remove:
        cur_search_object.pop(key, None)
    
    return cur_search_object

config = Config()

def load_from_yaml(path):
  """Loads the configuration from a YAML file.

  You should only call it once per program since it updates the global `config` values.

  Args:
    path (str): Path of the configuration file
  
  """

  with open(path, mode='r', encoding='utf-8') as f:
    config.update(yaml.load(f))
  
  # Configure the logging facility straight in!
  logging.basicConfig(**config.get('logging', {
    'level': 'WARNING'
  }))
