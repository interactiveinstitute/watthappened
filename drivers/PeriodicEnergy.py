# -*- coding: utf-8 -*-

import datetime

from energykit import Driver, EnergyIndicator, IOLoop, Time

class PeriodicEnergy(Driver):
  priority = 0

  def __init__(self, name, energy, holidays, times, timezone):
    super(PeriodicEnergy, self).__init__()
    self.name = name
    self.energy = energy
    self.holidays = holidays
    self.times = times
    self.timezone = timezone

    # We might decide to accept more complex time structures later, but for now:
    assert type(times is tuple) and len(times) is 2

    # TODO store buffer of last 3 lunches, and update card

  def run(self):
    self.data = self.load_or_create_data(self.energy.source, self.name)
    self.data.output = {}

    self.log('initializing')

    start = self.energy.domain()[0].next_at(self.times[0])
    duration = Time(self.times[1]) - Time(self.times[0])
    end = Time(Time.now() - duration)
    starts = start.range(end=end, freq='B', tz=self.timezone)
    for start in starts:
      if start.strftime('%Y%m%d') in self.holidays: continue
      self._store_energy((Time(start), Time(start + duration)))

    self.log('initialized')

    self.data.save()

    IOLoop.current().add_timeout(datetime.timedelta(hours=1), self.run)

  def _store_energy(self, period):
    indicator = EnergyIndicator(self.energy, *period)
    key = period[0].strftime('%Y%m%d')
    self.data.output[key] = {
      'feed': self.energy.event_feed_name(),
      'sp_bubble': {
        'timestamp_start': period[0].as_ms(),
        'timestamp_end': period[1].as_ms(),
        'tags': ['period', self.name],
        'value': indicator.value(),
        'value_type': 'Wh',
        'priority': self.priority,
        'note': self.name
      }
    }
