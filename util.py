
from datetime import datetime
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


def covertFirebaseTimeToPythonTime(timestamp):
    timestamp = timestamp.rfc3339()
    try:
        print("orig")
        date_time_obj = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        print("except")
        date_time_obj = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    return date_time_obj
