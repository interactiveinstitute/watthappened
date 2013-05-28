# times can be either datetime or a timestamp int

class DataStream(object):
  instances = {}

  def __init__(self, **attrs):
    if attrs in self.instances:
      raise Warning('Use the %s.get factory method to get an instance.'
          % self.__class_.__name__)

    self._attrs = attrs

  @classmethod
  def get(cls, **attrs):
    if attrs in cls.instances:
      instance = cls.instances[attrs]
    else:
      instance = cls.instances[attrs] = cls(**attrs)
    return instance

  def value_at(self, time):
    raise NotImplementedError

  def last_measured_value(self):
    raise NotImplementedError

  def value_difference(self, start_time, end_time):
    raise NotImplementedError
