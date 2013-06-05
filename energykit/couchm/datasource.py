import couchdbkit
import restkit

import energykit

from datastream import *

class DataSource(energykit.DataSource, energykit.PubSub):
  def __init__(self, server, user, password, database):
    energykit.DataSource.__init__(self)
    energykit.PubSub.__init__(self)

    auth = restkit.BasicAuth(user, password)
    server = couchdbkit.Server(uri=server, filters=[auth])
    self.db = server.get_db(database)

    self._listening = False

  def _update_info(self):
    info = self.db.list('energy_data/feeds_and_datastreams',
        'by_source_and_time', group_level=1)
    self._feeds = info['feeds']
    self._datastreams = info['datastreams']

    # We'll use these indices to interpret query results.
    self._at_idx = info['at_idx']
    self._datastream_idx = info['datastream_idx']

  def get_stream_keys(self, allow_cached=True):
    if not '_datastreams' in dir(self) or not allow_cached:
      self._update_info()
    return [(f, ds) for f in self._feeds for ds in self._datastreams]

  def _create_stream_instance_by_key(self, key):
    if not '_datastreams' in dir(self):
      self._update_info()
    return DataStream(self, key)

  def _listen(self, include_last_changes=0):
    update_seq = self.db.info()['update_seq'] - include_last_changes
    stream = couchdbkit.changes.ChangesStream(self.db,
                                              feed='continuous',
                                              filter='energy_data/measurements',
                                              heartbeat=True,
                                              since=update_seq,
                                              include_docs=True)
    self._listening = True

    def callback(change):
      doc = change['doc']
      time = energykit.Time.from_ms(doc['timestamp'])
      for key in self._datastreams:
        if key in doc:
          source = self.get_stream_by_key((doc['source'], key))
          value = doc[key]
          datapoint = energykit.DataPoint(time, value)
          self.publish(datapoint, source)

    def run(callback):
      for change in stream: callback(change)

    energykit.run_async(run, callback)
