from atlas_sdk import Skill

def intent_handler(request):
  print (request.lang)

with Skill.from_config('atlas.yml') as s:
  s.handle('example_intent', intent_handler)

  input ('Press any key to stop')