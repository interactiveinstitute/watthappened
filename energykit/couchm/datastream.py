import energykit
from energykit import util

from _couch import *

class DataStream(energykit.DataStream):
  def _key(self, timestamp):
    return db.show('energy_data/unix_to_couchm_ts', '',
                   feed=self._feed_name, timestamp=milliseconds)

  def value_at(self, time):
    ts = util.timestamp(time)
    result = db.view('energy_data/by_source_and_time',
                     startkey=[self._feed_name],
                     endkey=self._key(ts))
    if len(result):
      value = result.first()['value']
      return value[at_idx], value[datastream_idx[datastream]]
    else:
      return None, 0

  def last_measured_value(self):
    result = _couch.db.view('energy_data/by_source_and_time',
                            startkey=[self._feed_name],
                            endkey=[self._feed_name, {}])
    value = result.first()['value']
    return value[_couch.at_idx], value[_couch._datastream_idx[self._name]]

  def value_difference(self, start_time, end_time):
    start_time, start_value = self.value_at(start_time)
    end_time, end_value = self.value_at(end_time)
    return end_value - start_value
