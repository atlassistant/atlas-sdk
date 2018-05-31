import logging

class Facade:
  """Represents a tiny wrapper to make it easy for object to communicate with the
  outside world.
  """

  def __init__(self):
    self._logger = logging.getLogger(self.__class__.__name__.lower())

  def activate(self):
    """Activates a facade by doing some initialization stuff if needed by subclasses.
    """

    self._logger.debug('Activating facade')
  
  def deactivate(self):
    """Deactivate this facade. It may be usefull if you have some cleanup stuff to process.
    """
    
    self._logger.debug('Deactivating facade')