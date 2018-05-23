from .client import Client, INTENT_TOPIC, DISCOVERY_PING_TOPIC, DISCOVERY_PONG_TOPIC
from .request import Request
from .broker import BrokerConfig
from .version import __version__, __version_requirements__
from semantic_version import Version, Spec
import logging, argparse, sys, json, os, gettext, sys

I18N_LOCALE_DIR = 'locale'
I18N_DOMAIN_NAME = 'messages'

class SkillClient(Client):
  """Main class when you want to describe and register an Atlas skill.

  """
  
  def __init__(self, name, version, author=None, description=None, intents=[], env=[]):
    """Initialize a new Skill.

    :param name: Name of the skill
    :type name: str
    :param version: Version of the skill
    :type version: str
    :param author: Author of the skill
    :type author: str
    :param description: Optional description of the skill
    :type description: str
    :param intents: List of intents supported by this skill
    :type intents: list
    :param env: List of configuration variables needed by this skill
    :type env: list

    """

    super(SkillClient, self).__init__(name='sdk')

    self.name = name
    self.author = author
    self.version = version
    self.description = description
    self.intents = intents
    self.env = env
    self._version_specs = Spec(__version_requirements__)
    self._translations = {}

    self.log.info('Created skill %s\n\t%s' % (self, '\n\t'.join([s.__str__() for s in self.env])))
    
    self._load_translations()

  def __str__(self):
    return '%s %s - %s' % (self.name, self.version, self.description or 'No description')

  def _load_translations(self):
    """Load translations for this skill by using python builtin gettext.
    """

    script_dir = sys.path[0]
    locale_dir = os.path.join(script_dir, I18N_LOCALE_DIR)

    self.log.info('Loading translations from %s' % locale_dir)

    if os.path.isdir(locale_dir):
      for ldir in os.listdir(locale_dir):
        self._translations[ldir] = gettext.translation(I18N_DOMAIN_NAME, localedir=I18N_LOCALE_DIR, languages=[ldir])
        self.log.debug('Loaded translations for %s' % ldir)

  def on_connect(self, client, userdata, flags, rc):
    super(SkillClient, self).on_connect(client, userdata, flags, rc)

    self.subscribe_json(DISCOVERY_PING_TOPIC, self.on_discovery_request)

    def make_handler(handler):
      return lambda d, r: self._on_intent(handler, d, r)

    for intent in self.intents:
      topic = INTENT_TOPIC % intent.name  
      self.subscribe_json(topic, make_handler(intent.handler))

    # Sends a pong immediately so skill could attach to atlas asap
    self._pong()

  def _on_intent(self, handler, data, raw):
    """Called when a handler should be called.

    :param handler: Handler to call
    :type handler: callable
    :param data: JSON data received
    :type data: dict
    :param raw: Raw payload
    :type raw: str

    """

    # TODO i'm not sure if it's good for the localization part

    request = Request(self, data, raw)

    self._translations.get(request.lang, gettext).install(I18N_DOMAIN_NAME)

    handler(request)

  def on_discovery_request(self, data, raw):
    self.log.debug('Discovery request from %s' % data)

    version_str = data.get('version')

    if version_str:
      if not self._version_specs.match(Version(version_str)):
        self.log.warn('atlas version %s did not match skill requirements %s! Things could go wrong!' % (version_str, __version_requirements__))

    self._pong()

  def _pong(self):
    """Sends a discovery pong.
    """

    self.publish(DISCOVERY_PONG_TOPIC, json.dumps({
      'name': self.name,
      'author': self.author,
      'description': self.description,
      'version': self.version,
      'intents': { i.name: [s.name for s in i.slots] for i in self.intents },
      'env': { e.name: str(e.type) for e in self.env }
    }))

  def run(self):
    """Parses current os args and run the MQTT loop.
    """

    parser = argparse.ArgumentParser(description='Atlas SDK %s' % __version__)

    parser.add_argument('-H', '--host', help='MQTT host address')
    parser.add_argument('-p', '--port', help='MQTT port', type=int)
    parser.add_argument('-u', '--user', help='Username and password for the mqtt in the form user:password')

    args = parser.parse_args(sys.argv[1:])

    # TODO yeah I know that's a bit ugly

    user, pwd = (args.user or ':').split(':', 1)

    args_dict = {
      'host': args.host,
      'port': args.port,
      'username': user,
      'password': pwd,
    }
    
    try:
      self.start(BrokerConfig(**{ k: v for k,v in args_dict.items() if v != None }), False)
    except Exception as e:
      self.log.debug(e)
      self.log.info('Stopping %s' % self.name)