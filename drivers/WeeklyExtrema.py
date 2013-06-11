from energykit import Driver, PowerExtremaIndicator, Time

class WeeklyExtrema(Driver):
  priority = 0

  def __init__(self, power_stream):
    super(WeeklyExtrema, self).__init__()
    self.power = power_stream

  def run(self):
    self.data = self.load_or_create_data(self.power.source)
    self.data.output = {}
    self.log('(re)calculating past extrema, this may take a while...')
    for week in Time.weeks_around(self.power.domain()[0], Time.now()):
      self._set_indicator(week)
    self.data.save()
    self.log('(re)calculated past extrema')
    self._update_handlers(self.indicator.subscribe)

  def _set_indicator(self, week):
    self.indicator = PowerExtremaIndicator(self.power, *week)

    key = week[0].as_week()
    try:
      min, max = self.indicator.datapoints()
      for name in ('min', 'max'): self._set(key, name, locals()[name])
    except ValueError:
      # The indicator had no datapoints.
      pass

    # Store latest week with data: this week's data might be updated.
    self.data.cache['week_key'] = key
    self.data.cache['week_start'] = week[0].as_ms()

  def _set(self, week_key, name, dp):
    week_id = week_key + '/' + name
    value = str('dFdt' in dir(dp.value) and dp.value.dFdt or dp.value)
    self.data.output[week_id] = {
      'feed': self.power.event_feed_name(),
      'sp_bubble': {
        'timestamp': dp.time.as_ms(),
        'tags': ['%simum' % name],
        'value': value,
        'value_type': 'W',
        'priority': self.priority
      }
    }

  def _update_handlers(self, which):
    which(self._on_update, 'min')
    which(self._on_update, 'max')
    which(self._week_ended, 'ended')

  def _on_update(self, datapoint, type):
    self._set(self.data.cache['week_key'], type, datapoint)
    self.data.save()
    self.log('updated', type)

  def _week_ended(self, data, topic):
    self._update_handlers(self.indicator.unsubscribe)
    self._set_indicator(next(Time.weeks_around(Time.now())))
    self._update_handlers(self.indicator.subscribe)
