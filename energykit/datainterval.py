class DataInterval(object):
  def __init__(self, stream, start_time=None, end_time=None):
    self.stream = stream
    self.start_time = start_time
    self.end_time = end_time

  def last_measured_value(self):
    raise NotImplementedError

  def value_difference(self):
    raise NotImplementedError

  def highest_value(self, start_time, end_time):
    raise NotImplementedError

  def lowest_value(self, start_time, end_time):
    raise NotImplementedError

  def peak_period(self, length, start_time, end_time):
    # e.g. the best hour during 2013
    raise NotImplementedError

  def extrema(self):
    raise NotImplementedError
