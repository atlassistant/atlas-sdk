import logging, gettext, sys, os
from .pubsubs import PubSub
from .runnable import Runnable
from .adapters import SkillAdapter
from .config import load_from_yaml, config
from .constants import NAME_KEY, DESCRIPTION_KEY, VERSION_KEY, AUTHOR_KEY, INTENTS_KEY, \
  SETTINGS_KEY, I18N_DOMAIN_NAME, I18N_LOCALE_DIR
from .request import Request

def intent_handler(skill, handler):
  """Skill specific handler to convert raw data to a Request object.

  Args:
    adapter (Skill): Skill to use
    handler (callable): Handler to call
  Returns:
    callable: Lambda to run the handler with a Request arg

  """

  # Inner method which will setup the i18n module upon request reception
  def trigger(data):
    req = Request(skill._adapter, data)
    skill._install_translation(req.lang)
    handler(req)

  return lambda data: trigger(data)

class Skill(Runnable):
  """A skill executes action based on intents parsed by the NLU.

  You must register your skill to specific intents and your handlers will be called by
  atlas when the intent has been recognized. Atlas will send you each slot that it
  will extract and start a conversation for your skill to ask for whatever it needs
  to accomplish its work.
  
  """

  def __init__(self, name, version, description=None, author=None, intents={}, settings=[], adapter=None):
    """Initialize a new skill.

    Args:
      name (str): Name of the skill
      version (str): Version of the skill
      description (str): Optional description
      author (str): Optional author
      intents (dict): Dictionary of intents managed by your skill with associated slots
      settings (list): List of settings key used by this skill, their value will be send by atlas on intent request
      adapter (SkillAdapter): Adapter to use to communicate with the outside world

    """

    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self.name = name
    self.version = version
    self.author = author
    self.description = description
    self.intents = intents
    self.settings = settings

    self._adapter = adapter or SkillAdapter(PubSub.from_config())
    self._adapter.attach({
      NAME_KEY: self.name,
      VERSION_KEY: self.version,
      AUTHOR_KEY: self.author,
      DESCRIPTION_KEY: self.description,
      INTENTS_KEY: self.intents,
      SETTINGS_KEY: self.settings,
    })

    self._translations = {}

  def handle(self, intent, handler):
    """Subscribe for a given intent.

    Args:
      intent (str): Intent name to handle
      handler (callable): Handler to call, it will received a Request object

    """

    self._adapter.handle(intent, intent_handler(self, handler))

  def _install_translation(self, lang):
    """Setup the gettext for the given language.

    Args:
      lang (str): Language to setup

    """

    if not lang:
      return
      
    self._translations.get(lang, gettext).install(I18N_DOMAIN_NAME)

  def _load_translations(self):
    """Loads the translation available.
    """

    script_dir = sys.path[0]
    locale_dir = os.path.join(script_dir, I18N_LOCALE_DIR)

    self._logger.info('Loading translations from %s' % locale_dir)

    if os.path.isdir(locale_dir):
      for lang in os.listdir(locale_dir):
        self._translations[lang] = gettext.translation(I18N_DOMAIN_NAME, locale_dir=I18N_LOCALE_DIR, languages=[lang])
        self._logger.debug('Loaded %s translations' % lang)

  def run(self):
    self._load_translations()
    self._adapter.activate()

  def cleanup(self):
    self._adapter.deactivate()

  @classmethod
  def from_config(cls, path):
    """Instantiates a new skill based on the configuration file given.

    Args:
      path (str): Path to the configuration file
    Returns:
      Skill: A skill instance

    """

    load_from_yaml(path)

    return Skill(**config.get('skill', {}))