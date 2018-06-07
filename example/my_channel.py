from atlas_sdk import Channel

def created(data):
  print ('Channel created: %s' % data)

def asked(data):
  print ('Asked! %s' % data)

with Channel('example_channel_id', on_ask=asked, on_created=created):
  input('Press any key to return')

