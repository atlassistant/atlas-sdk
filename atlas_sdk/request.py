from .client import DIALOG_ASK_TOPIC, DIALOG_SHOW_TOPIC, DIALOG_TERMINATE_TOPIC
import json, random

CID_KEY = '__cid'
SID_KEY = '__sid'
UID_KEY = '__uid'
LANG_KEY = '__lang'
VERSION_KEY = '__version'
ENV_KEY = '__env'

def random_select(element):
  """If the given parameter is a list, a random item will be selected.

  :param element:
  :type element: list or str
  :rtype: str

  """

  if type(element) is list:
    return random.choice(element)

  return element

class Request():
  """Represents a wrapper around a single message request with handy methods
  to ease the development of skills.
  """
  
  def __init__(self, client, data, raw):
    """Constructs a new request object.

    :param client: Skill client to use
    :type client: SkillClient
    :param data: Json data of the message
    :type data: dict
    :param raw: Raw message
    :type raw: str

    """

    self._client = client

    self.data = data
    self.raw = raw

    # Extract common properties

    self.cid = data.get(CID_KEY)
    self.sid = data.get(SID_KEY)
    self.uid = data.get(UID_KEY)
    self.lang = data.get(LANG_KEY)
    self.version = data.get(VERSION_KEY)

  def env(self, key):
    """Retrieve a configuration key for this request.

    :param key: Key to retrieve
    :type key: str

    """

    return self.data.get(ENV_KEY, {}).get(key)

  def slot(self, name, default=None, converter=None):
    """Handy method to retrieve a slot value for this request.

    :param name: Slot name to retrieve
    :type name: str
    :param default: Default value if not found
    :type default: any
    :param converter: Converter to use to transform the parameter if set
    :type converter: callable
    
    """

    slot = self.data.get(name, default)

    if converter and slot:
      if type(slot) is list:
        return [converter(v) for v in slot]
      else:
        return converter(slot)

    return slot

  def ask(self, slot, text, choices=None, additional_data={}):
    """Asks a question to the user to require its inputs.

    :param slot: Name of the slot attached to this question
    :type slot: str
    :param text: Text to show to the user, if a list is given, a random element will be choose
    :type text: list or str
    :param choices: Choices proposed to the user, used to restrict valid values
    :type choices: list
    :param additional_data: Additional data to add to the payload
    :type additional_data: dict

    """

    additional_data.update({
      CID_KEY: self.cid,
      'text': random_select(text),
      'slot': slot,
      'choices': choices,
    })

    self._client.publish(DIALOG_ASK_TOPIC % self.sid, json.dumps(additional_data))

  def show(self, text, additional_data={}, terminate=False):
    """Presents data to the user.

    :param text: Text to show to the user, if a list is given, a random element will be choose
    :type text: list or str
    :param additional_data: Additional data to add to the payload
    :type additional_data: dict
    :param terminate: Wether or not the dialog should be terminated
    :type terminate: bool

    """

    additional_data.update({
      CID_KEY: self.cid,
      'text': random_select(text),
    })
    
    self._client.publish(DIALOG_SHOW_TOPIC % self.sid, json.dumps(additional_data))

    if terminate:
      self.terminate()

  def terminate(self):
    """Terminates the dialog for this request. It informs the system that the skill
    has ended its work.
    
    """

    self._client.publish(DIALOG_TERMINATE_TOPIC % self.sid, json.dumps({
      CID_KEY: self.cid,
    }))