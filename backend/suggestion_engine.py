from datetime import datetime, time, timedelta

def get_free_slots(schedule, block_minutes=60):
    study_start = time(8, 0)   # 8:00 AM
    study_end = time(22, 0)    # 10:00 PM
    step = timedelta(minutes=15)

    suggestions = []

    for day, busy_blocks in schedule.items():
        current = datetime.combine(datetime.today(), study_start)
        end_of_day = datetime.combine(datetime.today(), study_end)

        # Convert busy time blocks to datetime objects for comparison
        busy_dt = [
            (
                datetime.combine(datetime.today(), start),
                datetime.combine(datetime.today(), end)
            ) for start, end in busy_blocks
        ]

        while current + timedelta(minutes=block_minutes) <= end_of_day:
            slot_end = current + timedelta(minutes=block_minutes)

            overlap = any(
                (slot_start < block_end and slot_end > block_start)
                for block_start, block_end in busy_dt
                for slot_start in [current]
            )

            if not overlap:
                suggestions.append({
                    "day": day,
                    "start": current.strftime("%I:%M %p"),
                    "end": slot_end.strftime("%I:%M %p")
                })

            current += step

    return suggestions

# 🧪 Test it
if __name__ == "__main__":
    from schedule_parser import load_schedule
    schedule = load_schedule("../data/Sample Student Schedule Data/schedule1.json")
    slots = get_free_slots(schedule, block_minutes=90)
    for s in slots[:5]:
        print(f"{s['day']}: {s['start']} → {s['end']}")
