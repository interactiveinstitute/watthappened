from ektime import *

class Value(object):
  def __init__(self, *args):
    self.set(*args)

  def set(self):
    raise NotImplementedError

  def current(self):
    return self.predicted_at(Time.from_s(time.time()))

  def predicted_at(self, time):
    raise NotImplementedError

  def predicted_time_when(self, value):
    raise NotImplementedError

class PiecewiseLinearValue(Value):
  def set(self, dF=0, dt=1, t1=1, F0=0):
    '''
    dF is the difference in the primitive of the value
    dt is the time window duration in which the value was measured, in s
    t1 is the end of the time window, as a Time object
    F0 is the value of the primitive at t1-dt, or 0

    e.g. a plugwise measurement:
    energy E(t0, t1) = dF[Ws] with dt = t1-t0[s] and F0 = E(0, t0)
      given by F0 = E(0, t0), F1 = E(0, t1) = F0+dF, dt=t1-t0
    power P(t1) = dF[Ws]/1[s] = dF[W] over interval [t1-dt, t1) with dt=1
      given by dF, dt=1, t1=now

    e.g. if we express presence as 1p or 0p, and presence time as 'pseconds':
    presence q(t1) = dF[ps]/1[s] = dF[p] in {0,1} over interval " with "
    prestime Q(t0, t1) = dF[ps] with dt = t1-t0[s] and F0 = Q(0, t0)

    dF and F0 may be any vector value of the same type.
    '''
    if not self.zero:
      self.zero = dF * 0

    self.dF = dF
    self.dt = dt
    self.t1 = t1.as_s()
    self.t0 = self.t1 - dt
    if F0 is 0:
      self.F0 = self.zero
    else:
      self.F0 = F0

    self.dFdt = dF * (1. / dt)

  def predicted_at(self, time):
    t = time.as_s()
    assert t > self.t0
    return self.F0 + self.dFdt * (t - self.t0)

  def predicted_time_until(self, value):
    F1 = self.F0 + self.dF
    value += self.F0
    if ((value > F1 and self.dFdt > self.zero) or
        (value < F1 and self.dFdt < self.zero)):
      seconds = (value - self.F0) / self.dFdt - self.dt
    elif value == self.F0:
      seconds = 0
    else:
      seconds = float('inf')
    return seconds

class EnergyValue(PiecewiseLinearValue):
  unit = 'Ws'
  derivative = 'W'
  zero = 0

  @classmethod
  def from_power(cls, P, t=None):
    return cls(P, 1, t)

  @classmethod
  def from_energy(cls, t1, E1, t0=0, E0=0):
    return cls(E1 - E0, t1.as_s() - t0.as_s(), t1, E0)

  def as_W(self):
    return self.dFdt

  def as_Wh(self):
    return self.dF / 3600

  def current_as_Wh(self):
    return self.current()

class PresenceTimeValue(PiecewiseLinearValue):
  unit = 'presence s'
  derivative = 'presence'
  zero = 0

if __name__ == '__main__':
  print 'Tests (read the code):'
  print

  # PlugWise example input
  during_last_second = 0.042 # Wh
  t = Time()
  val = EnergyValue.from_power(during_last_second * 3600, t)
  print 'PlugWise reported %.1f W at %s.' % (val.as_W(), t)
  energy = val.predicted_at(Time.from_s(t.as_s() + 24 * 3600)) / 3600 / 1000
  print 'It this keeps going on for a day, that is %.1f kWh.' % energy
  print

  # Two (time [s], energy [Ws]) tuples
  datapoint1 = (Time.from_s(1370369092), 16.3 * 3600 * 1000)
  datapoint2 = (Time.from_s(1370382710), 22.1 * 3600 * 1000)
  val = EnergyValue.from_energy(*(datapoint2 + datapoint1))
  print '%(P).1f W * %(t).1f h = %(E).1f Wh' % {

    'P': val.as_W(),
    't': val.dt / 3600,
    'E': val.as_Wh()
  }
  kWh = 10.
  until = val.predicted_time_until(kWh * 3600 * 1000)
  print 'With this pace, you will reach 10 kWh after %.1f h.' % (until / 3600)

  sleep = 2
  first = val.current_as_Wh()
  time.sleep(sleep)
  second = val.current_as_Wh()
  difference = (second - first) / 3600
  print 'During the last %d seconds, %.1f Wh was added.' % (sleep, difference)
