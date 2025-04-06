document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("queryType");
    const askBtn = document.getElementById("submitBtn");
    const input = document.getElementById("customQuestion");
    const customAskBtn = document.getElementById("customAskBtn");
    const chatBox = document.getElementById("chatBox");
    const toggleDark = document.getElementById("toggleDark");
  
    // 🌙 Toggle dark mode
    toggleDark.addEventListener("click", () => {
      document.documentElement.classList.toggle("dark");
      const isDark = document.documentElement.classList.contains("dark");
      localStorage.setItem("darkMode", isDark);
    });
  
    // 🌙 Restore dark mode on load
    if (localStorage.getItem("darkMode") === "true") {
      document.documentElement.classList.add("dark");
    }
  
    // 💬 Append message to chat
    function addMessage(text, isUser = false) {
      const bubble = document.createElement("div");
      bubble.className = `flex ${isUser ? "justify-end" : "justify-start"}`;
  
      const inner = document.createElement("div");
      inner.className = `
        max-w-[80%] px-4 py-2 rounded-lg whitespace-pre-wrap break-words
        ${isUser
          ? "bg-green-600 text-white rounded-br-none"
          : "bg-blue-100 dark:bg-blue-700 text-gray-900 dark:text-white rounded-bl-none"}
      `;
      inner.textContent = text;
  
      bubble.appendChild(inner);
      chatBox.appendChild(bubble);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    // 🤖 Talk to backend
    async function askCopilot(question) {
      addMessage(`💬 ${question}`, true);
  
      try {
        const res = await fetch("http://localhost:5000/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question })
        });
  
        const data = await res.json();
        let responseText = "";
  
        if (data.assignments) {
          responseText = "📌 Assignments:\n" + data.assignments.map(a => `• ${a.title} (${a.course}) – due ${a.due_at}`).join("\n");
        } else if (data.grades) {
          responseText = "📊 Grades:\n" + data.grades.map(g => `• ${g.course}: ${g.grade}`).join("\n");
        } else if (data.courses) {
          responseText = "🎓 Enrolled Courses:\n" + data.courses.map(c => `• ${c}`).join("\n");
        } else if (data.day && data.start && data.end && data.room) {
          responseText = `📅 Suggested Study Time:\n• ${data.day} from ${data.start} to ${data.end} in ${data.room}`;
        } else if (data.message) {
          responseText = data.message;
        } else if (data.error) {
          responseText = "❌ " + data.error;
        } else {
          responseText = "🤖 That's out of my scope.";
        }
  
        addMessage(responseText);
      } catch (err) {
        addMessage("❌ Error: " + err.message);
      }
    }
  
    // 🧠 Ask based on dropdown
    askBtn.addEventListener("click", () => {
      const map = {
        assignments: "What assignments are due this week?",
        grades: "What are my grades?",
        courses: "What courses am I enrolled in?",
        study: "Suggest a study slot for this week"
      };
      const selected = dropdown.value;
      if (selected) {
        askCopilot(map[selected]);
        dropdown.value = "";
      }
    });
  
    // 💬 Ask from custom input
    customAskBtn.addEventListener("click", () => {
      const q = input.value.trim();
      if (q) {
        askCopilot(q);
        input.value = "";
      }
    });
  
    // 🔥 Send with Enter key
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        customAskBtn.click();
      }
    });
  });
  