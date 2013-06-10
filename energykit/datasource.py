class DataSource(object):
  '''An interface to a backend that receives and/or provides data.
  '''

  def __init__(self):
    self._instances = {}

  def get_stream_keys(self, allow_cached=True):
    raise NotImplementedError

  def get_stream_by_key(self, key):
    if not key in self._instances:
      self._instances[key] = self._create_stream_instance_by_key(key)
    return self._instances[key]

  def _create_stream_instance_by_key(self, key):
    raise NotImplementedError

  def write(self, data, time=None):
    'data is a dict combining DataStream: value maps; value is JSONifiable'
    raise NotImplementedError

  def load_driver_data(self, driver, id):
    raise NotImplementedError

  def save_driver_data(self, data):
    raise NotImplementedError
