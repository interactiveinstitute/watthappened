# -*- coding: utf-8 -*-

from config_priv import *

# Set this to n to also provide the last n changes to your change handler.
DEBUG_USE_LAST_CHANGES = 500

FAKE_STREAMS = range(8000, 8005)

def DRIVERS():
  import drivers
  from energykit import couchm, fake, EnergyIndicator, ValueType

  source = couchm.DataSource(**COUCHDB['sp'])
  p_all = source.get_stream_by_key(('allRooms', 'ElectricPower'))
  yield drivers.WeeklyExtrema(p_all)

  e_all = source.get_stream_by_key(('allRooms', 'ElectricEnergy'))
  e_all.enhance(p_all, ValueType.POWER)
  holidays = ('20130101', '20130106', '20130329', '2013401', '20130501',
      '20130509', '20130526', '20130606',
      '20130621', '20131101', '20131110', '20131223', '20131224',
      '20131225', '20131226', '20131231')
  lunch = ('11:30', '12:30')
  timezone = 'Europe/Stockholm'
  yield drivers.PeriodicEnergy('lunch', e_all, holidays, lunch, timezone)

  feed_names = {
    'room261': 'Lisa Ossman',
    'room241': 'Helena Nakos',
    'room242': 'Caroline Markusson',
    'room243': 'Anders Hjörnhede',
    'room244': 'Sven Hermansson',
    'room245': 'Roger Nordman',
    'room252': 'Pia Tiljander',
    'room253': 'Svein Ruud',
    'room254': 'Lennart Gustavsson',
    'room255': 'Carolina Hiller',
    'room256': 'Fredrik Niklasson',
    'room257': 'Johan Larsson',
    'room258': 'Peter Wahlgren',
    'room259': 'Sara Jensen',
    'room260': 'Ulla Lindberg',
  }
  feeds = dict([
    (source.get_stream_by_key((feed_name, 'ElectricEnergyUnoccupied')), name)
    for feed_name, name in feed_names.iteritems()
  ])
  yield drivers.IndividualContest('contest',
    'Lowest total absence energy this week',
    p_all, feeds, 'Wh', 'week', EnergyIndicator)

  yield drivers.StaticImage(p_all, 'data/about.png')
 
  '''
  source = couchm.DataSource(**COUCHDB['testbuilding'])

  fake_stream = fake.DataSource().get_stream_by_key(FAKE_STREAMS[0])
  couchm_test = source.get_stream_by_key(('testbuilding', 'ElectricPower'))

  yield drivers.Pipe(fake_stream, couchm_test)
  yield drivers.WeeklyExtrema(couchm_test)
  '''
