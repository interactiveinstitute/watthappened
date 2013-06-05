class DataPoint(object):
  def __init__(self, time=None, value=None, unit=None):
    self.time = time
    self.value = value
    self.unit = unit

  def is_empty(self):
    return time is None

  def __str__(self):
    return '(%s, %s)' % (self.time, self.value)
