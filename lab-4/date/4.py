import datetime

days = int(input())

def days_to_seconds(days):
    """Convert days into seconds."""
    return days * 24 * 60 * 60

x = datetime.datetime.now()
x1 = x + datetime.timedelta(days)

difference_in_days = (x1 - x).days

difference_in_seconds = days_to_seconds(difference_in_days)

print(f"Difference in seconds: {difference_in_seconds}")