#!/usr/bin/env python

from datetime import datetime

def get_ISO_to_unix(time):
    try:
        utc_dt = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S.%f')
    except Exception as e:
        print("Exception: {}".format(e))
        utc_dt = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
    # Convert UTC datetime to seconds since the Epoch
    timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
    return int(timestamp)
