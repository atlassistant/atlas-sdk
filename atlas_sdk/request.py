from .constants import META_SESSION_ID_KEY, META_CONVERSATION_ID_KEY, META_USER_ID_KEY, \
  META_LANG_KEY

class Request:
  """Wrapper around an intent request.

  It's used to make it more developer-friendly since it exposed all actions available
  when you received an intent request.

  """

  def __init__(self, adapter, data):
    """Instantiates a new request.

    Args:
      adapter (SkillAdapter): Adapter to use to communicate
      data (dict): Raw data sent by the atlas service

    """

    self._data = data
    self._adapter = adapter

    self.session_id = data.get(META_SESSION_ID_KEY)
    self.conversation_id = data.get(META_CONVERSATION_ID_KEY)
    self.user_id = data.get(META_USER_ID_KEY)
    self.lang = data.get(META_LANG_KEY)

  def slot(self, name):
    pass

  def ask(self):
    pass

  def answer(self):
    pass

  def end(self):
    """Ends the current conversation.
    """

    pass