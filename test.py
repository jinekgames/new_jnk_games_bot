import datetime

a = datetime.date.today()

b = datetime.date(a.year, a.month, a.day+1)

print(a, b)