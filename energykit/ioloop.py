import threading
import tornado.ioloop

from pubsub import *

_pubsub = PubSub()

class IOLoop(tornado.ioloop.IOLoop):
  pass

def run_async(run, callback):
  'Note: callback runs in the main loop, run in another thread'
  def actual_cb(*args, **kwargs):
    IOLoop.instance().add_callback(callback, *args, **kwargs)
  thread = threading.Thread(target=run, args=(actual_cb,))
  thread.daemon = True
  thread.start()

def start():
  try:
    IOLoop.current().start()
  except KeyboardInterrupt:
    IOLoop.current().stop()
    _pubsub.publish(True, 'stop')
    print

subscribe = _pubsub.subscribe
