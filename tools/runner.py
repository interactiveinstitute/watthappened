#!/usr/bin/env python

import config
import drivers
import energykit

class Runner(object):
  def run(self):
    for driver in config.DRIVERS():
      if 'run' in dir(driver):
        driver.run()
    energykit.start()

if __name__ == '__main__':
  runner = Runner()
  runner.run()
