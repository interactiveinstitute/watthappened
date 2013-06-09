import energykit

class DataInterval(energykit.DataInterval):
  def last_measured_value(self):
    if self.end_time:
      end_key = self.stream._key(self.end_time)
    else:
      end_key = [self.stream._feed_name, {}]
    result = self.stream.source.db.view('energy_data/by_source_and_time',
                                        startkey=[self.stream._feed_name],
                                        endkey=end_key)
    value = result.first()['value']
    return self.stream._to_point(result.first()['value'])

  def value_difference(self):
    start_point = self.stream.value_at(self.start_time)
    end_point = self.stream.value_at(self.end_time)
    return end_point.value - start_point.value

  def extrema(self):
    start_key = [self.stream._feed_name, self.stream._name]
    if self.start_time: start_key.append(self.start_time.as_ms())
    end_key = [self.stream._feed_name, self.stream._name]
    if self.end_time: end_key.append(self.end_time.as_ms())
    result = self.stream.source.db.view('energy_data/extrema',
                                        startkey=start_key,
                                        endkey=end_key,
                                        group_level=2)
    if len(result):
      def to_point(v):
        t = energykit.Time.from_ms(v[0])
        return energykit.DataPoint(t, self.stream._to_value(v[1], t))
      return map(lambda k: to_point(result.first()['value'][k]), ('min', 'max'))
    else:
      return None
