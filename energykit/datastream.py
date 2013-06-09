from pubsub import *
from value import *

# TODO(sander) implementations currently use strings for values while it would be cleaner to use the right Value subclasses.

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

  def observe(self, listener):
    raise NotImplementedError

  def write(self, value):
    raise NotImplementedError

  def domain(self):
    raise NotImplementedError

  def event_feed_name(self):
    return str(self.key)

  def __str__(self):
    return '<DataStream %s>' % str(self.key)
