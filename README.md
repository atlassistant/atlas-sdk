atlas-sdk
===

Python SDK for the [atlas](https://github.com/atlassistant/atlas) assistant!

## Installation

### PIP

You should use the version `< 2.0.0` with:

`pip install atlas-sdk==1.1.8`

### Source

`git clone` this repository and run `python setup.py install`. 

If you're a developer, prefer the command `python setup.py develop`.

## Usage

### SkillClient

Used this class to defines a new skill that should respond to given intents. This client already take care of the skill discovery routine to make it available to **atlas**.

```python
import logging
from atlas_sdk import SkillClient, Intent, Slot, Env, Request

def handle_echo(request):
  """Handle echo request.
  
  :type request: Request
  
  """

  # When calling request.slot, you retrieve a SlotData object which is a wrapper around a list of
  # values (since atlas could returns many values for a single slot based on user input.
  # It exposes some utility methods such as first() and last().
  date = request.slot('date').first().value

  # The "date" variable now contains the value extracted by Atlas

  if not date:
    # Ask for user input. Once done, this handler would be called again
    # If you pass a list as a second argument, a random element will be choose as the text, this make it
    # easy for your skill to propose some variants
    return request.ask('date', _('You should provide a date?!'))

  # Show something in the channel from which this request has been started
  # In request.env, you only have access to environment defined in the SkillClient,
  # since atlas does not send you all user settings.
  request.show(_('Hello from echo! Env was %s') % request.env('A_USELESS_PARAMETER'), terminate=True)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)

  echo_skill = SkillClient(
    name='Echo',
    description='Respond to echo intent',
    version='1.0.0',
    intents=[
      # Handle "echo" intent. When the NLU returns this intent, the agent will call this skill and our handler.
      # The slot arg is only used by the atlas discovery service.
      Intent('echo', handle_echo, slots=[Slot('date')]),
    ],
    env=[
      # This parameter will be retrieved and made available in the Request argument in your handlers. This parameter is available on a per user basis so each user can have its own set of parameters
      Env('A_USELESS_PARAMETER'),
    ],
  )

  echo_skill.run()
```

### ChannelClient

Used this tiny client to create your own Channel to communicate with **atlas**. A channel can be anything you want such as a Slack bot, a web client, a CLI, a sound system which may handle user inputs issued as voice commands.

## i18n

This SDK use the [standard python package](https://docs.python.org/3/library/i18n.html) to localize skills. A traditional workflow is as follow:

- Use `_('Your message text')` from your own code.
- Run `xgettext your_script.py -o messages.pot` to generates a translation model
- Copy the `.pot` file into a `.po` file representing your translation in the skill directory under `locale/<lang>/LC_MESSAGES`
- Generates a binary translation file with the command `msgfmt messages.po`