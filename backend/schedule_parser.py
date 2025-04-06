from datetime import datetime, timedelta
import json

# Map short day codes to full weekday names
DAY_MAP = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "R": "Thursday",
    "F": "Friday"
}

def parse_time_range(time_str):
    """Convert '02:00pm-03:15pm' to (datetime, datetime) pair."""
    start_str, end_str = time_str.split("-")
    start = datetime.strptime(start_str.strip(), "%I:%M%p").time()
    end = datetime.strptime(end_str.strip(), "%I:%M%p").time()
    return (start, end)

def load_schedule(filepath):
    """Parse JSON file and return busy times by weekday."""
    with open(filepath, "r") as f:
        data = json.load(f)

    schedule = {day: [] for day in DAY_MAP.values()}

    for course in data:
        for meeting in course.get("Meetings", []):
            days = meeting.get("Days", "")
            times = meeting.get("Times", "")
            if not days or not times:
                continue

            time_block = parse_time_range(times)
            for letter in days:
                weekday = DAY_MAP.get(letter)
                if weekday:
                    schedule[weekday].append(time_block)

    return schedule

# 🧪 Test it
if __name__ == "__main__":
    sched = load_schedule("../data/Sample Student Schedule Data/schedule1.json")
    for day, blocks in sched.items():
        print(f"{day}: {blocks}")
