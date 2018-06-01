import logging

class Adapter:
  """Represents a tiny wrapper to make it easy for object to communicate with the
  outside world.
  """

  def __init__(self):
    self._logger = logging.getLogger(self.__class__.__name__.lower())

  def activate(self):
    """Activates this adapter by doing some initialization stuff if needed by subclasses.
    """

    self._logger.debug('Activating adapter')
  
  def deactivate(self):
    """Deactivate this adapter. It may be usefull if you have some cleanup stuff to process.
    """
    
    self._logger.debug('Deactivating adapter')