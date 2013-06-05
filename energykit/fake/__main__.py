from __init__ import *

source = DataSource()

streams = (
  source.get_stream_by_key(8000),
  source.get_stream_by_key(8001),
)

print 'keys:', source.get_stream_keys()

for stream in streams:
  print 'set value at', 'http://localhost:%d/' % stream.key

def handler(datapoint, source):
  print 'change', datapoint, 'from', source

source.subscribe(handler)

energykit.start()
