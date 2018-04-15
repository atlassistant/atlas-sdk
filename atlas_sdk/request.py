from .client import DIALOG_ASK_TOPIC, DIALOG_SHOW_TOPIC, DIALOG_TERMINATE_TOPIC
import json

class Request():
  """Represents a wrapper around a single message request with handy methods
  to ease the development of skills.
  """
  
  def __init__(self, client, message):
    """Constructs a new request object.

    :param client: Skill client to use
    :type client: SkillClient
    :param message: Message attached to this request
    :type message: Message

    """

    self._client = client
    self._message = message

  def ask(self, slot, text, additional_data={}):
    additional_data.update({
      'text': text,
      'slot': slot,
    })

    self._client.publish(DIALOG_ASK_TOPIC % self._message.id, json.dumps(additional_data))

  def show(self, text, additional_data={}):
    additional_data.update({
      'text': text,
    })
    
    self._client.publish(DIALOG_SHOW_TOPIC % self._message.id, json.dumps(additional_data))

  def terminate(self):
    self._client.publish(DIALOG_TERMINATE_TOPIC % self._message.id)