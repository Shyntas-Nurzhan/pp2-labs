import datetime

x = datetime.datetime.now()

yesterday = x.day -1
today = x.day
tomorrow = x.day + 1

print(f"Yesterday it was the {yesterday}" +" "+ x.strftime("%B"))
print(f"Today it is {today}" +" "+ x.strftime("%B"))
print(f"Tomorrow it will be {tomorrow}" +" "+ x.strftime("%B"))