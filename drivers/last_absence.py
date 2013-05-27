# -*- coding: utf-8 -*-

import couchm

presence = { feed: False for feed in couchm.feeds }
absence_start_ts = { feed: 0 for feed in couchm.feeds }

def send_to_warhol(feed, json, recipe):
  print 'Sending %s to %s with data:' % (recipe, feed), json

def show_last_absence(feed, start_ts, end_ts):
  energy = couchm.energy_between(start_ts, end_ts, feed)
  hours = int((end_ts - start_ts) / 60 / 60 / 1000 * 10) / 10.
  if abs(hours) > 0.0001: power = energy / hours
  else: power = 0

  json = {
    'hours': hours,
    'power': power,
    'energy': energy
  }

  send_to_warhol(feed, json, 'your_last_absence')

def on_measurement(feed, datastream, value, timestamp, doc):
  print doc
  if datastream == 'OfficeOccupied':
    if presence[feed] != value:
      presence[feed] = value
      if value == True:
        show_last_absence(feed, absence_start_ts[feed], timestamp)
      elif value == False:
        absence_start_ts[feed] = timestamp
  elif datastream == 'ElectricEnergy':
    # see if there is a record?
    pass

couchm.listen_to_measurements(on_measurement)
