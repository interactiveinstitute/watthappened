import energykit
import tornado.web

class _Handler(tornado.web.RequestHandler):
  def initialize(self, stream):
    self.stream = stream

  def get(self):
    self.write_form()

  def post(self):
    value = self.get_argument('value', '50')
    if value: self.stream.set_value(value)
    self.write_form()

  def write_form(self):
    self.write('''
<!doctype html>
<title>Fake DataStream %d</title>
<form method=post>
  <p><i>P</i> = <input name=value type=number min=0 step=.5 value="%s" autofocus> W
</form>
''' % (self.stream.key, self.stream._value))

class _Ignorer(tornado.web.RequestHandler):
  def get(self):
    pass

class DataStream(energykit.DataStream):
  def __init__(self, source, port):
    super(DataStream, self).__init__(source, port)

    self._value = '50'
    self._time = energykit.Time.now()

    app = tornado.web.Application([
      (r'/', _Handler, dict(stream=self)),
      (r'/favicon.ico', _Ignorer),
    ])
    app.listen(port)

    print 'fake stream initialised at: http://localhost:%d/' % port

  def set_value(self, value):
    self._value = value
    self._time = energykit.Time.now()
    self.publish(self.get_datapoint(), self)

  def get_datapoint(self):
    return energykit.DataPoint(self._time, self._value)
