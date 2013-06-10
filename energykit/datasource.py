class DataSource(object):
  '''An interface to a backend that receives and/or provides data.
  '''

  def __init__(self):
    self._instances = {}

  def get_stream_keys(self, allow_cached=True):
    '''
    :param bool allow_cached: Set to False if a fresh index is required.

    :returns: Keys that can be used with :meth:`get_stream_by_key`.
    :rtype: list or generator
    '''
    raise NotImplementedError

  def get_stream_by_key(self, key):
    '''
    :param key: A key as specified by the implementation.
    :returns: The only instance with key :attr:`key`, possibly just generated.
    :rtype: an instance of a :class:`energykit.datastream.DataStream` subclass
    '''
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
