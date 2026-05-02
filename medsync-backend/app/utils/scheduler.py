from datetime import datetime, time, timedelta

def get_reminder_times(frequency_str: str):
    freq = frequency_str.lower()
    
    if "sos" in freq or "as needed" in freq:
        return [] 

    if "tds" in freq or "three times" in freq or "tid" in freq or "1-1-1" in freq:
        return [time(8, 0), time(14, 0), time(20, 0)]

    if "bid" in freq or "twice" in freq or "1-0-1" in freq:
        return [time(9, 0), time(21, 0)]

    if "6 hours" in freq or "q6h" in freq:
        return [time(6, 0), time(12, 0), time(18, 0), time(0, 0)]
    
    if "once" in freq or "daily" in freq or "1-0-0" in freq:
        return [time(9, 0)]
    
    return [time(10, 0)] 

def calculate_next_dose(reminder_times):
    now = datetime.now().time()

    for r_time in sorted(reminder_times):
        if r_time > now:
            return r_time

    return min(reminder_times)