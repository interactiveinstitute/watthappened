import datetime
import math
import pandas as pd
import time

class Time(pd.Timestamp):
  MONDAY = 0
  WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
      'Saturday', 'Sunday')

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

  def next_at(self, time_str):
    hours, minutes = time_str.split(':')
    candidate = Time(datetime.datetime(self.year, self.month, self.day,
      int(hours), int(minutes)))
    if candidate > self:
      return candidate
    else:
      # TODO(sander) how will this work with DST?
      return Time(candidate + datetime.timedelta(days=1))

  def range(self, *args, **kwargs):
    return pd.date_range(start=self, *args, **kwargs)

  # TODO(sander) could also be an instance method, t.previous_weekday(wd)
  @classmethod
  def previous_weekday(cls, time, weekday):
    days = time.weekday() - weekday
    if days > 0: days -= 8
    new = time + datetime.timedelta(days=days)
    return Time(datetime.datetime(new.year, new.month, new.day))

  @classmethod
  def weeks_around(cls, first, last=None):
    if last is None: last = first
    time = cls.previous_weekday(first, cls.MONDAY)
    week = datetime.timedelta(days=7)
    while time <= last:
      yield (Time(time), Time(time + week))
      time += week
