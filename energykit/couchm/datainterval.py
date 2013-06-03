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
