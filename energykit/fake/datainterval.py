import energykit

class DataInterval(energykit.DataInterval):
  def last_measured_value(self):
    return float(self.stream._value)
