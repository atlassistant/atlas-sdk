import logging
from atlas_sdk import SkillClient, Intent, Slot, Env

def handle_echo(request):
  print(request.data)

  request.ask('message', 'What about it?')

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)

  echo_skill = SkillClient(
    name='Echo',
    description='Respond to echo intent',
    version='1.0.0',
    intents=[
      Intent('echo', handle_echo, slots=[Slot('message')]),
      Intent('weather_forecast', handle_echo),
    ],
    env=[
      Env('A_USELESS_PARAMETER'),
    ],
  )
  echo_skill.run()