import config
from energykit import Driver

class Pipe(Driver):
  def __init__(self, source, sink):
    self.source = source
    self.sink = sink

  def run(self):
    self.source.subscribe(self._on_update)

  def _on_update(self, datapoint, source):
    self.sink.source.write({ self.sink.key: str(datapoint.value) })
    self.log('written', datapoint.value)
