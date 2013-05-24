import couchdbkit
import restkit
import time

import config

auth = restkit.BasicAuth(config.COUCHDB_USER, config.COUCHDB_PASSWORD)
server = couchdbkit.Server(uri=config.COUCHDB_SERVER, filters=[auth])

db = server.get_db(config.COUCHDB_DATABASE)

def now():
  return int(time.time() * 1000)

class Card(object):
  def __init__(self, feed, data, recipe, priority=0):
    self.feed = feed
    self.data = data
    self.recipe = recipe
    self.priority = priority

  def push(self):
    # TODO send to warhol
    pass

class Bubble(object):
  def __init__(self, feed, note, timestamp, value, value_type, priority=0, tags=[], card=None):
    self.feed = feed
    self.note = note
    self.timestamp = timestamp
    self.value = value
    self.value_type = value_type
    self.priority = priority
    self.tags = tags
    if card: print 'Attached cards are not yet supported'

  def push(self):
    db.save_doc({
      'source': self.feed,
      'timestamp': self.timestamp,
      'tags': self.tags,
      'note': self.note,
      'value': self.value,
      'value_type': self.value_type,
      'priority': self.priority,
    })

  @classmethod
  def push_about_power(cls, feed, note, timestamp, value, priority=0, tags=[], card=None):
    Bubble(feed, note, timestamp, value, 'power', priority, tags, card).push()

  @classmethod
  def push_about_energy(cls, feed, note, timestamp, value, priority=0, tags=[], card=None):
    Bubble(feed, note, timestamp, value, 'energy', priority, tags, card).push()

if __name__ == '__main__':
  Bubble.push_about_power('testroom', 'hello world', now(), 30)
