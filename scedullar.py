mmm19_scedullar = [
    # Mon
    'расписание на понедельник',
    # Tue
    'расписание на вторник',
    # Wed
    'расписание на среду',
    # Thu
    'расписание на четверг',
    # Fri
    'расписание на пятницу',
    # Sat
    'расписание на субботу',
    # Sun
    'расписание на воскресенье'
]

def weekday_ru_en(ru_day):
    if ru_day == 'пн':
        return 'Monday'
    elif ru_day == 'вт':
        return 'Tuesday'
    elif ru_day == 'ср':
        return 'Wednesday'
    elif ru_day == 'чт':
        return 'Thursday'
    elif ru_day == 'пт':
        return 'Friday'
    elif ru_day == 'сб':
        return 'Saturday'
    elif ru_day == 'вс':
        return 'Sunday'
    else:
        return False
    # 'вт': 'Tuesday',
    # 'ср': 'Wednesday',
    # 'чт': 'Thursday',
    # 'пт': 'Friday',
    # 'сб': 'Saturday',
    # 'вс': 'Sunday',