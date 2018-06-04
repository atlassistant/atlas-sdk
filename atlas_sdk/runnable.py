class Runnable:
  """Abstract class to represent a runnable element which owns a `run` and
  `cleanup` method.

  """

  def __enter__(self):
    self.run()
    return self
  
  def __exit__(self, type, value, traceback):
    self.cleanup()
  
  def run(self):
    """Runs this component. Prefer using this instance using the `with` keyword.
    """

    pass

  def cleanup(self):
    """Cleanup this component. Prefer using this instance using the `with` keyword.
    """

    pass