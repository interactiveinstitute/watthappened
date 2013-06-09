from energykit import Driver, Time, ValueType

class WeeklyExtrema(Driver):
  priority = 0
  _week_length = 7 * 24 * 60 * 60 * 1000

  def init(self, power_stream):
    self.power = power_stream
    self.power.type = ValueType.POWER

  def run(self):
    self.data = self.load_or_create_data(self.power.source)
    self.current_min = float('inf')
    self.current_max = float('-inf')

    first, last = self.power.domain()
    self.data.output = {}
    for week in Time.weeks_around(first, last):
      min, max = self.power.interval(Time(week[0]), Time(week[1])).extrema()
      key = Time(week[0]).as_week()
      for name in ('min', 'max'): self._set(key, name, locals()[name])

      # Store latest week with data: this week's data might be updated.
      self.data.cache['week_key'] = key
      self.data.cache['week_start'] = Time(week[0]).as_ms()
      self.current_min = min.value.as_W()
      self.current_max = max.value.as_W()
    # TODO(sander) handle case that no weeks have been added?

    self.data.save()
    self.power.observe(self._on_update)

  def _week_id(self, key, name):
    return '%s/%s' % (key, name)

  def _set(self, week_key, name, datapoint):
    week_id = self._week_id(week_key, name)
    if 'dFdt' in dir(datapoint.value): value = str(datapoint.value.dFdt)
    else: value = str(datapoint.value)
    self.data.output[week_id] = {
      'feed': self.power.event_feed_name(),
      'sp_bubble': {
        'timestamp': datapoint.time.as_ms(),
        'tags': ['%simum' % name],
        'value': value,
        'value_type': 'W',
        'priority': self.priority
      }
    }

  def _on_update(self, datapoint, source):
    value = float(datapoint.value)
    # TODO(sander) switch to next week if needed
    if value < self.current_min:
      self.current_min = value
      self._set(self.data.cache['week_key'], 'min', datapoint)
      self.log('updated minimum for', str(self.power.key))
      self.data.save()
    if value > self.current_max:
      self.current_max = value
      self._set(self.data.cache['week_key'], 'max', datapoint)
      self.log('updated maximum for', str(self.power.key))
      self.data.save()
