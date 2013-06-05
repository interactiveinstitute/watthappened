import pandas as pd

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

  def as_ms(self):
    return self.value / 1000

  def as_s(self):
    return self.value / 1000
