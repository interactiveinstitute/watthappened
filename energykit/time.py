import time

class Time(object):
  def __init__(self, milliseconds=None):
    if not milliseconds:
      milliseconds = int(round(time.time() * 1000))
    self._ms = milliseconds

  @classmethod
  def from_json(cls, time_str):
    raise NotImplementedError

  @classmethod
  def from_ms(cls, milliseconds):
    return cls(milliseconds)

  def as_ms(self):
    return self._ms
