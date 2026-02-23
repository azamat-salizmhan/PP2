# dates.py

from datetime import datetime, timedelta

today = datetime.now()
five_days_ago = today - timedelta(days=5)
print("Five days ago:", five_days_ago)

yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

no_microseconds = today.replace(microsecond=0)
print("Without microseconds:", no_microseconds)

date1 = datetime(2025, 1, 1, 0, 0, 0)
date2 = datetime(2025, 1, 2, 0, 0, 0)

difference = abs((date2 - date1).total_seconds())
print("Difference in seconds:", difference)
