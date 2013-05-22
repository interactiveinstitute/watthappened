# -*- coding: utf-8 -*-

COUCHDB_SERVER = 'http://aktivahuset.tii.se:8001'
COUCHDB_USER = '' # FIXME
COUCHDB_PASSWORD = '' # FIXME
COUCHDB_DATABASE = 'sp'

NON_DATASTREAM_FIELDS = ('timestamp', 'field', '_id', '_rev', '_deleted')

FIELDS = (
        'at',
        'ElectricPower',
        'OfficeOccupied',
        'OfficeTemperature',
        'ElectricEnergy',
        'ElectricEnergyOccupied',
        'ElectricEnergyUnoccupied'
      )

# Set this to n to also provide the last n changes to your change handler.
DEBUG_USE_LAST_CHANGES = 500
