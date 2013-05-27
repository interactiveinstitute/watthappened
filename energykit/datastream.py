# times can be either datetime or a timestamp int

class DataStream(object):
  instances = {}

  def __init__(self, feed_name, name):
    if (feed_name, name) in self.instances:
      raise Warning('Use the %s.get factory method to get an instance.'
          % self.__class_.__name__)

    self._feed_name = feed_name
    self._name = name

  @classmethod
  def get(cls, feed_name, name):
    if (feed_name, name) in cls.instances:
      instance = cls.instances[(feed_name, name)]
    else:
      instance = cls.instances[(feed_name, name)] = cls(feed_name, name)
    return instance

  def value_at(self, time):
    raise NotImplementedError

  def last_measured_value(self):
    raise NotImplementedError

  def value_difference(self, start_time, end_time):
    raise NotImplementedError
