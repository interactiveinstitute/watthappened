from pubsub import *
from value import *

class DataStream(PubSub):
  def __init__(self, source, key, type=ValueType.UNKNOWN):
    super(DataStream, self).__init__()

    self.source = source
    self.key = key
    self.type = type

  def value_at(self, time):
    raise NotImplementedError

  def interval(self, start_time=None, end_time=None):
    raise NotImplementedError

  def listen(self):
    raise NotImplementedError

  def write(self, value):
    raise NotImplementedError

  def domain(self):
    raise NotImplementedError

  def __str__(self):
    return '<DataStream %s>' % str(self.key)
