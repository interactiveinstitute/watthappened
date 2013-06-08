# -*- coding: utf-8 -*-

from config_priv import *

# Set this to n to also provide the last n changes to your change handler.
DEBUG_USE_LAST_CHANGES = 500

FAKE_STREAMS = range(8000, 8005)

def DRIVERS():
  import drivers
  from energykit import couchm, fake

  source = couchm.DataSource(**COUCHDB['testbuilding'])

  fake_stream = fake.DataSource().get_stream_by_key(FAKE_STREAMS[0])
  couchm_test = source.get_stream_by_key(('testbuilding', 'ElectricPower'))
  yield drivers.Pipe(fake_stream, couchm_test)

  yield drivers.WeeklyExtrema(couchm_test)
