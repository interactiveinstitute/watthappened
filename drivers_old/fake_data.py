import couchdbkit
import restkit
import time

import config

auth = restkit.BasicAuth(config.COUCHDB_USER, config.COUCHDB_PASSWORD)
server = couchdbkit.Server(uri=config.COUCHDB_SERVER, filters=[auth])

db = server.get_db(config.COUCHDB_DATABASE)

def now():
  return int(time.time() * 1000)

def set_fake_meter(timestamp, power, is_present, energy, presence_energy, absence_energy):
  'Add a measurement to testroom. Note: timestamp should be as returned by now().'

  db.save_doc({
    'source': 'testroom',
    'timestamp': timestamp,
    'ElectricPower': str(power),
    'OfficeOccupied': is_present,
    'ElectricEnergy': str(energy),
    'ElectricEnergyOccupied': str(presence_energy),
    'ElectricEnergyUnoccupied': str(absence_energy)
  })

if __name__ == '__main__':
  set_fake_meter(now(), 50.0, True, 1.0, 0.8, 0.2)

