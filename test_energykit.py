from energykit.couchm import *

feed = 'room241'
present = False
absence_start_ts = 0

occupied_stream = DataStream.get(feed_name=feed, name='OfficeOccupied')
energy_stream = DataStream.get(feed_name=feed, name='ElectricEnergy')
watch = Watch()

def show_last_absence(start_ts, end_ts):
  energy = energy_stream.value_difference(start_ts, end_ts)
  hours = int((end_ts - start_ts) / 60 / 60 / 1000 * 10) / 10.
  if abs(hours) > 0.0001: power = energy / hours
  else: power = 0

  json = {
    'hours': hours,
    'power': power,
    'energy': energy
  }

def on_presence_change(value, timestamp, **kwargs):
  if present != value:
    present = value
    if value == True:
      show_last_absence(absence_start_ts, timestamp)
    elif value == False:
      absence_start_ts = timestamp

watch.subscribe(on_presence_change, occupied_stream)
watch.start()
