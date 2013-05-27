import config
import energykit

from _couch import *
from datastream import *

class Watch(energykit.Watch):
  def start(self):
    update_seq = db.info()['update_seq'] - config.DEBUG_USE_LAST_CHANGES
    stream = couchdbkit.changes.ChangesStream(db,
                                              feed='continuous',
                                              heartbeat=True,
                                              since=update_seq,
                                              include_docs=True)
    try:
      for change in stream:
        doc = change['doc']
        if 'type' in doc and doc['type'] == 'measurement':
          for key in datastreams:
            if key in doc:
              self._publish(doc[key],
                            doc['timestamp'],
                            DataStream.get(doc['source'], key))
    except KeyboardInterrupt:
      pass
