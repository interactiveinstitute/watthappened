class DriverData(object):
  # TODO only provide output and cache fields to users (as list and dict)
  def __init__(self, source, driver, id):
    self.source = source
    self.driver = driver
    self.id = id
    self.cache = {}
    self.output = {}

  def save(self):
    self.source.save_driver_data(self)

  def __str__(self):
    return '<DriverData output=%s, cache=%s>' % (self.output, self.cache)

class Driver(object):
  'implement .init and/or .run, you may use energykit.run_async'

  def __init__(self, *args, **kwargs):
    if 'init' in dir(self):
      self.init(*args, **kwargs)

  def log(self, *message):
    print self.__class__.__name__ + ':', ' '.join(message)

  def load_data(self, source, id=None):
    data = source.load_driver_data(self, id)
    return data
  
  def load_or_create_data(self, source, id=None):
    data = self.load_data(source, id)
    if not data:
      data = DriverData(source, self, id)
    return data
