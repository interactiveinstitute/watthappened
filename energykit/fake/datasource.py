import energykit

from datastream import *

class DataSource(energykit.DataSource, energykit.PubSub):
  def __init__(self):
    energykit.DataSource.__init__(self)
    energykit.PubSub.__init__(self)

  def get_stream_keys(self, allow_cached=True):
    return self._instances.keys()

  def _create_stream_instance_by_key(self, key):
    stream = DataStream(self, key)
    stream.subscribe(self.publish)
    return stream
