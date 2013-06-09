// This script generates the _design/events design doc.

var ddoc = module.exports = {
  _id: '_design/events',
  views: {},
  filters: {}
}

// Emits ([source, timestamp]: bubble) pairs.
// To get all bubbles for myFeed between ts1 and ts2, query with
// startkey=["myFeed", ts1]&enkey=["myFeed", ts2]
ddoc.views.bubbles_by_feed_and_time = {
  map: function(doc) {
    if (doc.type == 'driverdata' && doc.output) {
      function each(obj, handler) {
        if (obj.length === undefined) for (var key in obj) handler(obj[key]);
        else obj.forEach(handler);
      }
      each(doc.output, function(value) {
        if (value.feed && value.sp_bubble)
          ['timestamp','timestamp_start','timestamp_end'].forEach(function(k) {
            if (value.sp_bubble[k])
              emit([value.feed, value.sp_bubble[k]], value.sp_bubble);
          })
      })
    }
  }
}

// Filter that allows docs containing bubbles.
// Optionally use a source parameter to filter by source.
ddoc.filters.bubbles = function(doc, req) {
  return doc.type == 'driverdata' &&
    doc.output &&
    doc.output.some(function(value) {
      return value.sp_bubble &&
        (!req.query.feed || req.query.feed == value.feed) })
}
