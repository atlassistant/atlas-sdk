from .constants import META_SESSION_ID_KEY, META_CONVERSATION_ID_KEY, META_USER_ID_KEY, \
  META_LANG_KEY, META_SETTINGS_KEY, TEXT_KEY, SLOT_KEY
from .config import Config
from .utils import choose_one

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
    self.settings = Config(data.get(META_SETTINGS_KEY, {}))

  def slot(self, name):
    pass

  def ask(self, slot, text):
    """Ask something to the user.

    Use this when you need user inputs to complete the request. Your handler
    will be called again with the slot filled.

    Args:
      slot (str): Slot to be filled
      text (str, list): Text to show to the user

    """

    self._adapter.ask({
      META_CONVERSATION_ID_KEY: self.conversation_id,
      SLOT_KEY: slot,
      TEXT_KEY: choose_one(text),
    })

  def answer(self, text, end_conversation=False):
    """Answer something to the user.

    Args:
      text (str, list): Text to show
      end_conversation (bool): Should it call `end` after answering

    """

    self._adapter.answer({
      META_CONVERSATION_ID_KEY: self.conversation_id,
      TEXT_KEY: choose_one(text),
    })

    if end_conversation:
      self.end()

  def end(self):
    """Ends the current conversation.
    """

    self._adapter.end({
      META_CONVERSATION_ID_KEY: self.conversation_id,
    })