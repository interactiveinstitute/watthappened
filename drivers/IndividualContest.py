# -*- coding: utf-8 -*-

import datetime

from energykit import Driver, IOLoop, Time

class IndividualContest(Driver):
  priority = 10

  def __init__(self, name, title, shared, streams, unit, interval, indicator):
    super(IndividualContest, self).__init__()
    self.name = name
    self.title = title
    self.shared = shared
    self.streams = streams
    self.unit = unit
    self.interval = interval
    self.indicator = indicator

    # We might decide to accept other durations later
    assert interval == 'week'

  def run(self):
    self.data = self.load_or_create_data(self.shared.source, self.name)
    self.data.output = {
      'card': {
        'feed': self.shared.event_feed_name(),
        'sp_card': {
          'tags': ['competition'],
          'timestamp': Time.now().as_ms(),
          'height': 512,
          'priority': self.priority,
          'class': 'competition'
        }
      }
    }

    self.log('initializing')

    html = '<h1>Competition leaders</h1><ul class="top3">'

    start_time = Time.previous_weekday(Time.now(), 0)
    end_time = Time.now()
    indicators = sorted([self.indicator(stream, start_time, end_time)
      for stream in self.streams.keys()], key=lambda ind: ind.value())
    for i in range(3):
      indicator = indicators[i]
      name = self.streams[indicator.energy].split(' ')[0]
      value = '± %d Wh' % (round(indicator.value() * 10) * 100)
      self.log('%d. %s with %s' % ((i + 1), name, value))

      html += '<li><div class="name">%s</div>' % name
      html += '<div class="value energy">%s</div></li>' % value

    html += '</ul><h2>%s</h2>' % self.title
    self.data.output['card']['sp_card']['content'] = html

    self.log('initialized')

    self.data.save()

    IOLoop.current().add_timeout(datetime.timedelta(hours=1), self.run)
