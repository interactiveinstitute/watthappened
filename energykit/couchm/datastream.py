import energykit

from datainterval import *

class DataStream(energykit.DataStream):
  def __init__(self, source, key):
    super(DataStream, self).__init__(source, key)

    self._feed_name = key[0]
    self._name = key[1]

  def _key(self, time):
    return db.show('energy_data/unix_to_couchm_ts', '',
                   feed=self._feed_name, timestamp=time.as_ms())

  def _to_point(self, value):
    time = energykit.Time.from_json(value[self.source._at_idx])
    value = value[self.source._datastream_idx[self._name]]
    return energykit.DataPoint(time, value)

  def value_at(self, time):
    result = db.view('energy_data/by_source_and_time',
                     startkey=[self._feed_name],
                     endkey=self._key(time))
    if len(result):
      return self._to_point(result.first()['value'])
    else:
      return energykit.DataPoint()

  def interval(self, start_time=None, end_time=None):
    return DataInterval(self, start_time, end_time)

  def listen(self):
    if not self.source._listening:
      self.source._listen()
