from pubsub import *

class DataStream(PubSub):
  def __init__(self, source, key):
    super(DataStream, self).__init__()

    self.source = source
    self.key = key

    source.subscribe(self.publish)

  def value_at(self, time):
    raise NotImplementedError

  def interval(self, start_time=None, end_time=None):
    raise NotImplementedError

  def listen(self):
    raise NotImplementedError
