import energykit

from datainterval import *

class DataStream(energykit.DataStream):
  def __init__(self, source, key, type=energykit.ValueType.UNKNOWN):
    super(DataStream, self).__init__(source, key, type)

    self._feed_name = key[0]
    self._name = key[1]

    source.subscribe(self.publish, self)

  def _key(self, time):
    return db.show('energy_data/unix_to_couchm_ts', '',
                   feed=self._feed_name, timestamp=time.as_ms())

  def _to_point(self, value):
    time = energykit.Time.from_json(value[self.source._at_idx])
    value = value[self.source._datastream_idx[self._name]]
    return energykit.DataPoint(time, value)

  def _to_value(self, value, t=None):
    if self.type is energykit.ValueType.POWER:
      return energykit.EnergyValue.from_power(value, t)
    else:
      return energykit.Value(value, t)

  def value_at(self, time):
    result = self.source.db.view('energy_data/by_source_and_time',
                     startkey=[self._feed_name],
                     endkey=self._key(time))
    if len(result):
      return self._to_point(result.first()['value'])
    else:
      return energykit.DataPoint()

  def interval(self, start_time=None, end_time=None):
    return DataInterval(self, start_time, end_time)

  def observe(self, listener):
    self.subscribe(listener, self)
    if not self.source._listening:
      self.source._listen()

  def domain(self):
    result = self.source.db.view('energy_data/domains', key=self._feed_name)
    if len(result):
      start = energykit.Time.from_ms(result.first()['value']['min'])
      end = energykit.Time.from_ms(result.first()['value']['max'])
      return (start, end)
    else:
      return None
