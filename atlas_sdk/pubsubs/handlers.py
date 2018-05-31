from json import loads

def json(handler):
  """Returns a lambda which will take a topic and raw data and call the handler
  with json deserialized data.

  Args:
    handler (callable): Handler to call with parsed json data
  Returns:
    callable: Lambda which takes topic and data

  """

  return lambda topic, data: handler(loads(data))

def data(handler):
  """Returns a lambda which will take a topic and raw data and call the handler
  with data only.

  Args:
    handler (callable): Handler to call with data
  Returns:
    callable: Lambda which takes topic and data

  """

  return lambda topic, data: handler(data)

def empty(handler):
  """Returns a lambda which call the handler without args.

  Args:
    handler (callable): Handler to call without parameters
  Returns:
    callable: Lambda which takes topic and data

  """

  return lambda topic, data: handler()