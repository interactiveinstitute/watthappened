import calendar
import datetime
import time

class Time(object):
  def __init__(self, milliseconds=None):
    #seconds = milliseconds / 1000
    #ContinuousValue.__init__(self, seconds, Time(0))
    if not milliseconds:
      milliseconds = int(round(time.time() * 1000))
    self._ms = milliseconds

  @classmethod
  def from_json(cls, time_str):
    # TODO(sander) this will probably cause timezone problems
    dt = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    ms = calendar.timegm(dt.utctimetuple()) * 1000
    return cls(ms)

  @classmethod
  def from_ms(cls, milliseconds):
    return cls(milliseconds)

  @classmethod
  def from_s(cls, seconds):
    return cls.from_ms(seconds * 1000)

  @classmethod
  def infinity(cls):
    return cls(float('inf'))

  def as_ms(self):
    return self._ms

  def as_s(self):
    return self._ms / 1000

  def __str__(self):
    return '<Time %s>' % str(self._ms / 1000)

  def __sub__(self, t):
    return Time(self._ms - t._ms)
