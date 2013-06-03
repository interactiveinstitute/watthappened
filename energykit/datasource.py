class DataSource(object):
  def __init__(self):
    self._instances = {}

  def get_stream_keys(self, allow_cached=True):
    raise NotImplementedError

  def get_stream_by_key(self, key):
    if not key in self._instances:
      self._instances[key] = self._create_stream_instance_by_key(key)
    return self._instances[key]
