# 🤖 Canvas Copilot: Your Smart Campus Assistant

## Overview

**Canvas Copilot** is an AI-powered assistant that integrates Canvas LMS data, Azure Vision Services, and student class schedules to help university students manage their academic life — all from one intuitive chatbot.

Whether it's checking your grades, finding upcoming assignments, or figuring out the best time and place to study, Canvas Copilot has you covered. Built for the **Canvas API Track (USF IT x Microsoft Hackathon)**.

---

## ✨ Key Features

- 🔗 **Canvas LMS Integration** – Fetch enrolled courses, grades, and assignment deadlines via Canvas API.
- 🧠 **Gemini AI Chat Assistant** – Natural language understanding to interpret and respond to student queries.
- 🧑‍💻 **Tailwind CSS Frontend** – Modern, responsive, dark-mode-enabled interface with chat UI and emoji-rich dropdown.
- 🧠 **Azure Vision + Custom Vision Model** – Detect live study space occupancy from synthetic study room images.
- ⏱️ **Smart Study Suggestions** – Suggest optimal time blocks based on student schedules and current room availability.
- 📅 **Schedule Summary** – Parse class schedules from JSON to show student meeting times.
- 💪 **Motivational Boosts** – Copilot offers words of encouragement when you need them.

---

## 📷 Demo

![Canvas Copilot UI](demo-screenshot.png)

---

## ⚙️ Tech Stack

| Tech | Purpose |
|------|---------|
| **Flask** | Backend API server |
| **Gemini API** | AI chat understanding |
| **Canvas LMS API** | Course, assignment, and grade data |
| **Azure AI Vision (Custom Vision)** | Study room occupancy detection |
| **Tailwind CSS** | UI styling and dark mode |
| **JavaScript** | Frontend interaction |
| **Python** | Core logic and APIs |

---

## 🗂 Project Structure

```
canvas-studyspace-copilot/
├── backend/
│   ├── app.py
│   ├── ai_helper.py
│   ├── canvas_api.py
│   ├── schedule_parser.py
│   ├── suggestion_engine.py
│   └── occupancy_detector.py
├── data/
│   ├── synthetic/ (Azure Vision dataset)
│   └── Sample Student Schedule Data/
├── frontend/
│   ├── index.html
│   └── script.js
└── .env
```

---

## 🚀 Running the App Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/canvas-studyspace-copilot.git
cd canvas-studyspace-copilot
```

### 2. Set up your environment
Create a `.env` file in the `/backend` folder:
```env
GEMINI_API_KEY=your_key
GEMINI_PROJECT_ID=your_project_id
CANVAS_API_TOKEN=your_canvas_token
AZURE_VISION_KEY=your_azure_key
AZURE_VISION_ENDPOINT=https://your-region.api.cognitive.microsoft.com/
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the backend
```bash
cd backend
python app.py
```

### 5. Open the frontend
Just open `index.html` in your browser!

---

## 💡 Example Prompts

| You ask... | Copilot replies... |
|------------|--------------------|
| "What are my grades?" | Lists all courses with visible grades |
| "Suggest a study slot" | Suggests best time and place based on schedule + room availability |
| "I'm free Monday at 5pm" | Matches you with a study block and an empty room |
| "How are you?" | Returns a friendly message and today's date |
| "What are my classes?" | Lists enrolled courses |
| "Motivate me" | Gives a quick motivational quote |

---

## 📌 Future Enhancements

- 📚 Add assignment details and instructor contacts
- 🕹️ Real-time study room camera integration
- 👥 Group study matching and availability
- 📲 Deploy to mobile/web for public access

---

## 🏁 Hackathon Track

**Canvas API Track – USF IT x Microsoft Hackathon 2025**  
Built in 24 hours with sleep-deprived passion and ✨ way too much coffee.
