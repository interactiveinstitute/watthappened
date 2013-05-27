import datetime

def timestamp(time):
  'returns the amount of milliseconds since unix epoch'

  # e.g. int(round(time.time() * 1000))

  if type(time) == datetime.datetime:
    # TODO(sander) do this right, with time zones
    raise ValueError('cannot convert from datetime yet')
  elif type(time) == int:
    return time
  else:
    raise ValueError('time type %s not supported' % type(time))
