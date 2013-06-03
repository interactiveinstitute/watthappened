from __init__ import *

import config

source = DataSource(**config.COUCHDB)

key = ('room241', 'ElectricPower')

keys = source.get_stream_keys()
assert key in keys

stream = source.get_stream_by_key(key)
print stream.interval().last_measured_value()
