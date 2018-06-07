from .constants import META_SESSION_ID_KEY, META_CONVERSATION_ID_KEY, META_USER_ID_KEY, \
  META_LANG_KEY, META_SETTINGS_KEY, TEXT_KEY, SLOT_KEY, CHOICES_KEY, CARDS_KEY
from .config import Config
from .slot_data import SlotData
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
    """Retrieve a slot values and wrap them in a SlotData instance.

    Args:
      name (str): Name of the slot to retrieve

    Returns:
      SlotData: SlotData instance

    """

    return SlotData(self._data.get(name))

  def ask(self, slot, text, choices=None, additional_data={}):
    """Ask something to the user.

    Use this when you need user inputs to complete the request. Your handler
    will be called again with the slot filled.

    Args:
      slot (str): Slot to be filled
      text (str, list): Text to show to the user
      choices (list): Optional list to propose to the user, used to restrict valid values
      additional_data (dict): Additional data to send

    """

    additional_data.update({
      META_CONVERSATION_ID_KEY: self.conversation_id,
      SLOT_KEY: slot,
      TEXT_KEY: choose_one(text),
      CHOICES_KEY: choices,
    })

    self._adapter.ask(additional_data)

  def answer(self, text, cards=None, additional_data={}, end_conversation=False):
    """Answer something to the user.

    Args:
      text (str, list): Text to show
      cards (obj, list): Cards to show to the user
      additional_data (dict): Additional data to send
      end_conversation (bool): Should it call `end` after answering

    """

    # Ensure we got an array first
    if cards and type(cards) is not list:
      cards = [cards]

    additional_data.update({
      META_CONVERSATION_ID_KEY: self.conversation_id,
      TEXT_KEY: choose_one(text),
      CARDS_KEY: cards,
    })

    self._adapter.answer(additional_data)

    if end_conversation:
      self.end()

  def end(self):
    """Ends the current conversation.
    """

    self._adapter.end({
      META_CONVERSATION_ID_KEY: self.conversation_id,
    })