from datetime import datetime, timedelta

def get_next_day(current_date, plus_day):
    date_obj = datetime.strptime(current_date, '%Y-%m-%d')
    next_day = date_obj + timedelta(days=plus_day)
    date_str = next_day.strftime('%Y-%m-%d')
    return date_str
