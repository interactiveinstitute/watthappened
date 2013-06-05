class Indicator(object):
  def get_current_value(self):
    raise NotImplementedError

  def get_current_time(self):
    raise NotImplementedError

  def get_current_datapoint(self):
    raise NotImplementedError
