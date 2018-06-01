import logging
from atlas_sdk import Channel
from atlas_sdk.adapters import ChannelAdapter
from atlas_sdk.pubsubs.mqtt_pubsub import MQTTPubSub

logging.basicConfig(level=logging.INFO)

pb = MQTTPubSub()

channel = Channel('example_channel_id', adapter=ChannelAdapter(pb))
other = Channel('another_channel_id', adapter=ChannelAdapter(pb))

channel.run()
other.run()

input('Press any key to return')

channel.cleanup()
other.cleanup()
