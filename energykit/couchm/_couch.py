import couchdbkit
import restkit

import config

_auth = restkit.BasicAuth(config.COUCHDB_USER, config.COUCHDB_PASSWORD)
_server = couchdbkit.Server(uri=config.COUCHDB_SERVER, filters=[_auth])

db = _server.get_db(config.COUCHDB_DATABASE)

_info = db.list('energy_data/feeds_and_datastreams', 'by_source_and_time', group_level=1)
feeds = _info['feeds']
datastreams = _info['datastreams']

# We'll use these indices to interpret query results.
at_idx = _info['at_idx']
datastream_idx = _info['datastream_idx']
