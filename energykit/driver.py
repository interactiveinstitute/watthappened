class Driver(object):
  'implement .__init__ and/or .run, you may use energykit.run_async'

  def log(self, *message):
    print self.__class__.__name__ + ':', ' '.join(message)
