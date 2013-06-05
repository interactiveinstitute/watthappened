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
    return self.value / 1000

  def as_s(self):
    return self.value / 1000
