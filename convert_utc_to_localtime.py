# reference: http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand

import calendar
from datetime import datetime, timedelta

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

now_is = datetime.utcnow()
converted = utc_to_local(now_is)

print "UTC TIME:", now_is
print "LOCAL TIME:", converted

