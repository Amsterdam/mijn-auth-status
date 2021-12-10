import math
from datetime import datetime, timedelta, timezone


def get_user_info(user):
    # TMA sessions are valid for 15 minutes
    validity_datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    # Timestamp in whole milliseconds (because that's what Javascript wants)
    timestamp = math.floor(validity_datetime.timestamp() * 1000)

    return {
        "isAuthenticated": True,
        "userType": user["type"].name,
        "validUntil": timestamp,
    }
