from ektime import *
from ioloop import *
from pubsub import *
from value import *

class Indicator(PubSub):
  def __init__(self):
    super(Indicator, self).__init__()

  def datapoints(self):
    '''
    :rtype: generator
    '''
    raise NotImplementedError

class EnergyIndicator(Indicator):
  def __init__(self, energy_stream, start_time, end_time):
    super(EnergyIndicator, self).__init__()

    self.energy = energy_stream
    self.energy.type = ValueType.ENERGY

    self.interval = self.energy.interval(start_time, end_time)

  def value(self):
    return self.interval.enhanced_value_difference()

class PowerExtremaIndicator(Indicator):
  '''
  :param energykit.datastream.DataStream power_stream:
  :param energykit.ektime.Time start_time:
  :param energykit.ektime.Time end_time:
  '''
  def __init__(self, power_stream, start_time, end_time):
    super(PowerExtremaIndicator, self).__init__()

    self.power = power_stream
    self.power.type = ValueType.POWER

    self.interval = self.power.interval(start_time, end_time)

    self.current_min = float('inf')
    self.current_max = float('-inf')

    self._timeout = None

  def datapoints(self):
    extrema = self.interval.extrema()
    if extrema:
      for extremum in self.interval.extrema():
        yield extremum
    else:
      return
      yield

  def subscribe(self, listener, topic=None):
    if self.interval.end_time < Time.now():
      raise Exception('Cannot subscribe to intervals excluding now')

    super(PowerExtremaIndicator, self).subscribe(listener, topic)

    points = [point for point in self.datapoints()]
    if len(points) == 2:
      min, max = points
      self.current_min = float(min.value.dFdt)
      self.current_max = float(max.value.dFdt)
    else:
      self.current_min = float('inf')
      self.current_max = float('-inf')

    self.interval.stream.subscribe(self._on_update)

    if self._timeout is None:
      deadline = self.interval.end_time - Time.now()
      self._timeout = IOLoop.current().add_timeout(deadline, self._on_timeout)

  def unsubscribe(self, listener, topic=None):
    super(PowerExtremaIndicator, self).unsubscribe(listener, topic)

    if self.subscription_count() == 0:
      self.interval.stream.unsubscribe(self._on_update)

      IOLoop.current().remove_timeout(self._timeout)

  def _on_update(self, datapoint, source):
    t = datapoint.time
    if t < self.interval.start_time or t > self.interval.end_time: return
    value = float(datapoint.value)
    if value < self.current_min:
      self.current_min = value
      self.publish(datapoint, 'min')
    if value > self.current_max:
      self.current_max = value
      self.publish(datapoint, 'max')

  def _on_timeout(self):
    self.publish(True, 'ended')
