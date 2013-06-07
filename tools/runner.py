#!/usr/bin/env python

import config
import drivers
import energykit

class Runner(object):
  def __init__(self):
    self.drivers = []

    self.setup()

  def run(self):
    for driver in self.drivers:
      if 'run' in dir(driver):
        driver.run()
    energykit.start()

  def setup(self):
    from energykit import couchm, fake

    def add(driver): self.drivers.append(driver)

    source = fake.DataSource() \
        .get_stream_by_key(config.FAKE_STREAMS[0])
    sink = couchm.DataSource(**config.COUCHDB['testbuilding']) \
        .get_stream_by_key(('testbuilding', 'ElectricPower'))
    add(drivers.Pipe(source, sink))

if __name__ == '__main__':
  runner = Runner()
  runner.run()
