"""This file contains all topics available through atlas.
"""

# atlas lifecycle events

ATLAS_STATUS_LOADING = 'atlas/status/loading'
ATLAS_STATUS_LOADED = 'atlas/status/loaded'
ATLAS_STATUS_UNLOADING = 'atlas/status/unloading'
ATLAS_STATUS_UNLOADED = 'atlas/status/unloaded'

ATLAS_REGISTRY_SKILL = 'atlas/registry/skill'

# Dialog related topics, communication with an agent

DIALOG_END_TOPIC = 'atlas/%s/dialog/end'
DIALOG_PARSE_TOPIC = 'atlas/%s/dialog/parse'
DIALOG_ASK_TOPIC = 'atlas/%s/dialog/ask'
DIALOG_ANSWER_TOPIC = 'atlas/%s/dialog/answer'

# Topic where request would be made available

INTENT_TOPIC = 'atlas/intents/%s'

# Channel related topics

CHANNEL_ASK_TOPIC = 'atlas/%s/channel/ask'
CHANNEL_ANSWER_TOPIC = 'atlas/%s/channel/answer'
CHANNEL_WORK_TOPIC = 'atlas/%s/channel/work'
CHANNEL_END_TOPIC = 'atlas/%s/channel/end'
CHANNEL_CREATE_TOPIC = 'atlas/%s/channel/create'
CHANNEL_CREATED_TOPIC = 'atlas/%s/channel/created'
CHANNEL_DESTROY_TOPIC = 'atlas/%s/channel/destroy'
CHANNEL_DESTROYED_TOPIC = 'atlas/%s/channel/destroyed'