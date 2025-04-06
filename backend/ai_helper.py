import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro-latest",
    generation_config={ "temperature": 0.6, "max_output_tokens": 256 },
    safety_settings={ 
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    }
)

system_prompt = """
You are Canvas Copilot, an AI assistant for university students. When a student asks a question, reply ONLY with JSON like:
{
  "intent": "get_course_grades",
  "filters": {
    "course": "PHY2049"
  }
}

Valid intents:
- get_upcoming_assignments
- get_course_grades
- get_courses
- get_course_info
- get_assignment_details
- suggest_study_slot
- followup_study_slot
- schedule_summary
- motivate_student
- casual_response
- out_of_scope
"""

def process_question(question):
    try:
        response = model.generate_content([system_prompt, question])
        if not response.candidates:
            raise ValueError("No valid Gemini response")
        text = response.text.strip().strip("```json").strip("```").strip()
        return json.loads(text)
    except Exception as e:
        print("[❌ Gemini Fallback]:", e)
        return fallback_logic(question)

def fallback_logic(q):
    q = q.lower()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if any(day in q for day in days) and any(x in q for x in ["am", "pm", ":"]):
        return {
            "intent": "suggest_study_slot",
            "filters": { "preferred_time": q }
        }

    if "assign" in q:
        return {"intent": "get_upcoming_assignments", "filters": {}}
    if "grade" in q:
        return {"intent": "get_course_grades", "filters": {}}
    if "course" in q:
        return {"intent": "get_courses", "filters": {}}
    if "study" in q:
        return {"intent": "followup_study_slot", "message": "When would you like to study?"}
    if "how are you" in q or "today" in q:
        return {
            "intent": "casual_response",
            "message": f"I'm good! Today is {datetime.now().strftime('%A, %B %d')}."
        }

    return {
        "intent": "out_of_scope",
        "message": "That's out of my scope. Try asking about classes, grades, or study time!"
    }
