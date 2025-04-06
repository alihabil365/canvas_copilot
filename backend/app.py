from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
from ai_helper import process_question
from canvas_api import get_upcoming_assignments, get_course_grades, get_all_courses
from schedule_parser import load_schedule
from suggestion_engine import get_free_slots
from occupancy_detector import detect_occupancy_from_image_url

load_dotenv()
app = Flask(__name__)
CORS(app)

STUDENT_SCHEDULE_PATH = "../data/Sample Student Schedule Data/schedule1.json"

ROOM_IMAGES = {
    "LIB": "https://raw.githubusercontent.com/USFGDSC/Canvas-API-Data/main/Canvas%20API%20Dataset/synthetic/LIB_full_ai.png",
    "ENB": "https://raw.githubusercontent.com/USFGDSC/Canvas-API-Data/main/Canvas%20API%20Dataset/synthetic/ENB_empty_ai.png",
    "MDN": "https://raw.githubusercontent.com/USFGDSC/Canvas-API-Data/main/Canvas%20API%20Dataset/synthetic/MDN_full_ai.png"
}

@app.route("/ask", methods=["POST"])
def ask_canvas():
    data = request.get_json()
    question = data.get("question", "")
    ai_response = process_question(question)

    intent = ai_response.get("intent")
    filters = ai_response.get("filters", {})

    try:
        if intent == "get_upcoming_assignments":
            return jsonify(get_upcoming_assignments(filters))

        elif intent == "suggest_study_slot":
            try:
                preferred_time = filters.get("preferred_time", "").strip().lower()
                schedule = load_schedule(STUDENT_SCHEDULE_PATH)
                free_slots = get_free_slots(schedule, block_minutes=90)

                if not free_slots:
                    return jsonify({ "message": "No free study times found in your schedule." })

                def extract_hour(time_str):
                    try:
                        return datetime.strptime(time_str, "%I:%M %p").hour
                    except:
                        return None

                # Case A: User gave preferred time (e.g., "Monday 5pm")
                if preferred_time and len(preferred_time.split()) >= 2:
                    try:
                        day_part, time_part = preferred_time.split()
                        preferred_hour = datetime.strptime(time_part, "%I%p" if "am" in time_part or "pm" in time_part else "%I:%M%p").hour

                        matched_slot = next((slot for slot in free_slots
                            if day_part.lower() in slot["day"].lower()
                            and abs(extract_hour(slot["start"]) - preferred_hour) <= 1), None)

                        if matched_slot:
                            room = next((r for r, url in ROOM_IMAGES.items()
                                if not detect_occupancy_from_image_url(url).get("occupied", True)), None)

                            return jsonify({
                                "day": matched_slot["day"],
                                "start": matched_slot["start"],
                                "end": matched_slot["end"],
                                "room": room or "No empty rooms available"
                            })
                        else:
                            return jsonify({ "message": f"No free study time found around {preferred_time}." })

                    except Exception as parse_error:
                        return jsonify({ "message": f"Could not understand your time: {str(parse_error)}" })

                # Case B: No preferred time → return any good slot
                room = next((r for r, url in ROOM_IMAGES.items()
                    if not detect_occupancy_from_image_url(url).get("occupied", True)), None)

                return jsonify({
                    "day": free_slots[0]["day"],
                    "start": free_slots[0]["start"],
                    "end": free_slots[0]["end"],
                    "room": room or "No empty rooms available"
                })
            except Exception as e:
                return jsonify({ "error": str(e) }), 500
            
        elif intent == "motivate_student":
            return jsonify({
                "message": "📣 You've got this! Stay focused and remember, one step at a time leads to big wins!"
            })

        elif intent == "get_course_grades":
            return jsonify(get_course_grades(filters))

        elif intent == "get_courses":
            return jsonify(get_all_courses())

        elif intent == "casual_response":
            return jsonify({ "message": ai_response.get("message", "🙂") })

        elif intent == "out_of_scope":
            return jsonify({ "message": ai_response.get("message", "❌ Out of scope.") })

        elif intent == "get_assignment_details":
            return jsonify({
                "info": "Assignment details feature is under development. For now, try asking about upcoming assignments!"
            })

        elif intent == "schedule_summary":
            schedule = load_schedule(STUDENT_SCHEDULE_PATH)
            summary = [f"{cls['Subject']} {cls['Name']} at {meet['Times']} on {meet['Days']}" 
                       for cls in schedule for meet in cls['Meetings']]
            return jsonify({"summary": summary})
        
        elif intent == "followup_study_slot":
            return jsonify({
                "message": ai_response.get("message", "When would you like to study?")
            })

        else:
            return jsonify({ "error": f"Unknown intent: {intent}" }), 400

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(debug=True)
