import datetime
import math
import pandas as pd

from energykit import Driver, Time

def _weeks_around(first, last):
  first -= datetime.timedelta(days=7)
  first = Time(datetime.datetime(first.year, first.month, first.day))
  n_weeks = int(math.ceil((last - first).days / 7.))
  times = pd.date_range(first, periods=n_weeks, freq='W-MON')
  previous = None
  for time in times:
    if previous: yield (previous, time)
    else: previous = time

class WeeklyExtrema(Driver):
  def init(self, power_stream):
    self.power = power_stream

  def run(self):
    self.data = self.load_or_create_data(self.power.source)

    first, last = self.power.domain()
    for week in _weeks_around(first, last):
      extrema = self.power.interval(Time(week[0]), Time(week[1])).extrema()
      print extrema
    # TODO loop through stream's week intervals, query extrema and store bubbles
    # TODO store extrema of current week (thus far) in bubble
    # TODO store pointer to current week in cache
    #self.data.save()
    self.power.subscribe(self._on_update)

  def _on_update(self, datapoint, source):
    self.log('update', datapoint.value)
    # TODO if this exceeds a current extremum, update that and save data
