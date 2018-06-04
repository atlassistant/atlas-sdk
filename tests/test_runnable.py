import unittest
from atlas_sdk.runnable import Runnable
from unittest.mock import MagicMock

class RunnableTests(unittest.TestCase):
  
  def test_with(self):
    runnable = Runnable()
    runnable.run = MagicMock()
    runnable.cleanup = MagicMock()

    with runnable as r:
      self.assertIsNotNone(r)
      runnable.run.assert_called_once()
      runnable.cleanup.assert_not_called()

    runnable.cleanup.assert_called_once()