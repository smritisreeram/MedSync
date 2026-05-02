from app.utils.scheduler import get_reminder_times, calculate_next_dose
from datetime import datetime

print("--- Testing Frequency Mapping ---")
test_cases = ["Three times a day", "Once daily", "Every 6 hours", "BID"]

for case in test_cases:
    times = get_reminder_times(case)
    print(f"Input: {case} -> Reminder Times: {[t.strftime('%H:%M') for t in times]}")

print("\n--- Testing Next Dose Calculation ---")
current_time = datetime.now().strftime("%H:%M")
print(f"Current System Time: {current_time}")

example_times = get_reminder_times("Three times a day") 
next_dose = calculate_next_dose(example_times)
print(f"For 'Three times a day', your next dose is at: {next_dose.strftime('%H:%M')}")