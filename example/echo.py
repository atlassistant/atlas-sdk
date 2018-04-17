import logging
from atlas_sdk import SkillClient, Intent, Slot, Env, Request

def handle_echo(request):
  """Handle echo request.
  
  :type request: Request
  
  """

  print(request.cid)
  print(request.slot('date'))

  request.show('Hello from echo!')

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)

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