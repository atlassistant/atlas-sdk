atlas-sdk
===

Python SDK for the [atlas](https://github.com/atlassistant/atlas) assistant!

## Installation

*pip maybe...*

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

  date = request.slot('date') # Returns the value of the 'date' slot if set

  if not date:
    # Ask for user input. Once done, this handler would be called again
    return request.ask('date', 'You should provide a date?!')

  # Show something in the channel from which this request has been started
  request.show('Hello from echo! Env was %s' % request.env('A_USELESS_PARAMETER'), terminate=True)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)

  echo_skill = SkillClient(
    name='Echo',
    description='Respond to echo intent',
    version='1.0.0',
    intents=[
      # Handle "echo" intent. When the NLU returns this intent, the agent will call this skill and our handler
      Intent('echo', handle_echo, slots=[Slot('message')]),
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
