# -*- coding: utf-8 -*-

import couchdbkit
import restkit

import config

auth = restkit.BasicAuth(config.COUCHDB_USER, config.COUCHDB_PASSWORD)
server = couchdbkit.Server(uri=config.COUCHDB_SERVER, filters=[auth])

db = server.get_db(config.COUCHDB_DATABASE)

info = db.list('energy_data/feeds_and_datastreams', 'by_source_and_time', group_level=1)
feeds = info['feeds']
datastreams = info['datastreams']

# We’ll use these indices to interpret query results.
at_idx = info['at_idx']
datastream_idx = info['datastream_idx']

def now():
  return int(round(time.time() * 1000))

def key(feed, milliseconds):
  return db.show('energy_data/unix_to_couchm_ts', '', feed=feed, timestamp=milliseconds)

def value_at(ts, feed, datastream):
  result = db.view('energy_data/by_source_and_time', startkey=[feed], endkey=key(feed, ts))
  if len(result):
    value = result.first()['value']
    return value[at_idx], value[datastream_idx[datastream]]
  else:
    return None, 0

def last_value(ts, feed, datastream):
  result = db.view('energy_data/by_source_and_time', startkey=[feed], endkey=[feed, {}])
  value = result.first()['value']
  return value[at_idx], value[datastream_idx[datastream]]

def energy_between(start, end, feed):
  start_time, start_energy = value_at(start, feed, 'ElectricEnergy')
  end_time, end_energy = value_at(end, feed, 'ElectricEnergy')
  return end_energy - start_energy

def listen_to_measurements(callback):
  update_seq = db.info()['update_seq'] - config.DEBUG_USE_LAST_CHANGES
  stream = couchdbkit.changes.ChangesStream(db,
                                            feed='continuous',
                                            heartbeat=True,
                                            since=update_seq,
                                            include_docs=True)
  try:
    for change in stream:
      doc = change['doc']
      if 'type' in doc and doc['type'] == 'measurement':
        for key in datastreams:
          if key in doc:
            callback(feed=doc['source'], datastream=key, value=doc[key], timestamp=doc['timestamp'], doc=doc)
  except KeyboardInterrupt:
    pass
