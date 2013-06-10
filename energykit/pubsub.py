class PubSub(object):
  def __init__(self):
    self._subscriptions = {}

  def publish(self, data=None, source=None):
    heard = []
    if source in self._subscriptions.keys():
      for listener in self._subscriptions[source]:
        listener(data, source)
        heard.append(listener)
    if None in self._subscriptions.keys():
      for listener in self._subscriptions[None]:
        if not listener in heard:
          listener(data, source)

  def subscribe(self, listener, source=None):
    if source in self._subscriptions.keys():
      subscriptions = self._subscriptions[source]
    else:
      subscriptions = []
      self._subscriptions[source] = subscriptions
    subscriptions.append(listener)

  def unsubscribe(self, listener, source=None):
    if source in self._subscriptions.keys():
      if listener in self._subscriptions[source]:
        self._subscriptions[source].remove(listener)

  def subscription_count(self):
    count = 0
    for source in self._subscriptions.keys():
      count += len(self._subscriptions[source])
    return count
