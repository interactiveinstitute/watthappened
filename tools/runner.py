#!/usr/bin/env python

import config
import drivers
import energykit

class Runner(object):
  def __init__(self):
    self.drivers = []

    config.DRIVERS(self.drivers.append)

  def run(self):
    for driver in self.drivers:
      if 'run' in dir(driver):
        driver.run()
    energykit.start()

if __name__ == '__main__':
  runner = Runner()
  runner.run()
