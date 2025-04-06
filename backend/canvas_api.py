
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()
API_BASE = "https://usflearn.instructure.com/api/v1"
TOKEN = os.getenv("CANVAS_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def get_course_id_map():
    resp = requests.get(f"{API_BASE}/courses?enrollment_state=active&per_page=100", headers=HEADERS)
    if not resp.ok:
        return {}

    return {
        f"course_{c['id']}": c["name"]
        for c in resp.json()
        if "name" in c and "id" in c
    }

def format_course_name(name):
    if not name:
        return "Unknown"
    parts = name.split()
    code = parts[0].split(".")[0]
    return f"{code} - {' '.join(parts[1:])}" if len(parts) > 1 else code

def get_upcoming_assignments(filters):
    response = requests.get(f"{API_BASE}/users/self/upcoming_events", headers=HEADERS)
    if not response.ok:
        return {"error": "Failed to fetch assignments", "details": response.text}

    events = response.json()
    eastern = pytz.timezone("US/Eastern")
    course_id_map = get_course_id_map()
    formatted = []

    for e in events:
        title = e.get("title", "Untitled")
        course_code = e.get("context_code")
        course_name = course_id_map.get(course_code, "Unknown")
        raw_due = e.get("assignment", {}).get("due_at")
        if not raw_due:
            continue

        try:
            utc_dt = datetime.strptime(raw_due, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
            local_due = utc_dt.astimezone(eastern)
        except Exception:
            continue

        formatted.append({
            "title": title,
            "course": format_course_name(course_name),
            "due_at": local_due.strftime("%A, %b %d at %I:%M %p"),
            "due_date": local_due.strftime("%Y-%m-%d"),
            "priority": "high" if "MUST DO" in title.upper() else "normal",
            "due_dt_obj": local_due
        })

    formatted = sorted(formatted, key=lambda x: x["due_dt_obj"])
    return {"assignments": [{k: a[k] for k in a if k != "due_dt_obj"} for a in formatted[:5]]}

def get_course_grades(filters):
    resp = requests.get(f"{API_BASE}/courses?enrollment_state=active&per_page=100", headers=HEADERS)
    if not resp.ok:
        return {"error": "Failed to fetch courses", "details": resp.text}

    results = []
    for course in resp.json():
        cid = course.get("id")
        cname = course.get("name")
        if not cid or not cname:
            continue

        enroll_url = f"{API_BASE}/courses/{cid}/enrollments?enrollment_state=active"
        gresp = requests.get(enroll_url, headers=HEADERS)

        if gresp.ok:
            for enrollment in gresp.json():
                if enrollment["type"] == "StudentEnrollment":
                    score = enrollment.get("grades", {}).get("current_score")
                    if score is not None:
                        results.append({
                            "course": format_course_name(cname),
                            "grade": f"{score:.2f}%"
                        })

    return {"grades": results}

def get_all_courses():
    resp = requests.get(f"{API_BASE}/courses?enrollment_state=active&per_page=100", headers=HEADERS)
    if not resp.ok:
        return {"error": "Failed to fetch courses", "details": resp.text}

    return {
        "courses": [
            format_course_name(c["name"])
            for c in resp.json()
            if "name" in c
        ]
    }
