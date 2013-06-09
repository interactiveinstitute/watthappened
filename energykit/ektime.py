import datetime
import math
import pandas as pd
import time

class Time(pd.Timestamp):
  @classmethod
  def from_json(cls, time_str):
    return cls(time_str)

  @classmethod
  def from_ms(cls, milliseconds):
    return cls(milliseconds * 1000000)

  @classmethod
  def from_s(cls, seconds):
    return cls.from_ms(seconds * 1000)

  @classmethod
  def infinity(cls):
    return float('inf')

  @classmethod
  def now(cls):
    return cls.from_ms(int(time.time() * 1000))

  def as_ms(self):
    return self.value / 1000000

  def as_s(self):
    return self.as_ms() / 1000

  def as_week(self):
    return '%03d%02d' % (self.year, self.week)

  @classmethod
  def weeks_around(cls, first, last=None):
    if last is None:
      last = first + datetime.timedelta(days=1)
      # TODO(sander) this might be buggy, should write tests
    first -= datetime.timedelta(days=7)
    first = Time(datetime.datetime(first.year, first.month, first.day))
    n_weeks = int(math.ceil((last - first).days / 7.))
    times = pd.date_range(first, periods=n_weeks, freq='W-MON')
    previous = None
    for time in times:
      if previous: yield (previous, time)
      else: previous = time
