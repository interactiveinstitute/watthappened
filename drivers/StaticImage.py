# -*- coding: utf-8 -*-

import base64
import os

from energykit import Driver, Time

class StaticImage(Driver):
  priority = 0

  def __init__(self, stream, file_name):
    super(StaticImage, self).__init__()
    self.stream = stream
    self.file_name = file_name 

  def run(self):
    self.data = self.load_or_create_data(self.stream.source, self.file_name)

    path = os.path.dirname(os.path.realpath(__file__)) + '/' + self.file_name

    with open(path, 'rb') as image_file:
      encoded_string = base64.b64encode(image_file.read())

    self.data.output = {
      'card': {
        'feed': self.stream.event_feed_name(),
        'sp_card': {
          'timestamp': Time.now().as_ms(),
          'tags': ['about', 'general'],
          'priority': self.priority,
          'class': 'staticImage',
          'height': 512,
          'content': 'data:image/png;base64,' + encoded_string
        }
      }
    }

    self.data.save()
