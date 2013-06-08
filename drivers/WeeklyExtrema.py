from energykit import Driver

class WeeklyExtrema(Driver):
  def init(self, stream):
    self.stream = stream

  def run(self):
    self.data = self.load_or_create_data(self.stream.source)
    self.data.cache = {}
    self.data.save()
    self.stream.subscribe(self._on_update)

  def _on_update(self, datapoint, source):
    self.log('update', datapoint.value)
    self.write_to(self.source)
