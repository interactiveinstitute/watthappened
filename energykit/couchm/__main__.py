from __init__ import *

import config

source = DataSource(**config.COUCHDB)

key = ('room241', 'ElectricPower')
key = ('room256', 'ElectricPower')

keys = source.get_stream_keys()
assert key in keys

stream = source.get_stream_by_key(key)
print 'last measured value:', stream.interval().last_measured_value()

def handler(datapoint, source):
  print 'change', datapoint

stream.observe(handler)

energykit.start()
