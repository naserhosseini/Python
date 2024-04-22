from datetime import datetime

def dayOfTheWeek( day, month, year):
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    the_date = datetime(year=year, month=month, day=day)
    return week[the_date.weekday()]


print(dayOfTheWeek(30, 8, 2022))
