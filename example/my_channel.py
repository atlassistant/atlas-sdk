import logging
from atlas_sdk import Channel

logging.basicConfig(level=logging.INFO)

def asked(data):
  print ('Asked! %s' % data)

with Channel('example_channel_id', on_ask=asked):
  input('Press any key to return')

