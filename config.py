# -*- coding: utf-8 -*-

from config_priv import *

# Set this to n to also provide the last n changes to your change handler.
DEBUG_USE_LAST_CHANGES = 500

FAKE_STREAMS = range(8000, 8005)

def DRIVERS():
  import drivers
  from energykit import couchm, fake

  source = fake.DataSource() \
      .get_stream_by_key(FAKE_STREAMS[0])
  sink = couchm.DataSource(**COUCHDB['testbuilding']) \
      .get_stream_by_key(('testbuilding', 'ElectricPower'))
  yield drivers.Pipe(source, sink)
