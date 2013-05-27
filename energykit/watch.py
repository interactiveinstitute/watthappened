class Watch(object):
  def __init__(self):
    self._subscriptions = {}

  def _publish(self, value, timestamp, datastream):
    heard = []
    if datastream in self._subscriptions.keys():
      for listener in self._subscriptions[datastream]:
        listener(value, timestamp, datastream)
        heard += listener
    if None in self._subscriptions.keys():
      for listener in self._subscriptions[None]:
        if not listener in heard:
          listener(value, timestamp, datastream)

  def subscribe(self, listener, datastream=None):
    if datastream in self._subscriptions.keys():
      subscriptions = self._subscriptions[datastream]
    else:
      subscriptions = []
      self._subscriptions[datastream] = subscriptions
    subscriptions.append(listener)

  def start(self):
    raise NotImplementedError()
