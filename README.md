# 📺 YouTube → Article → Website Generator

Convert any YouTube video into a **professional article + complete website (HTML, CSS, JS)** using AI.

---

## 🚀 Features

- 🔗 Input YouTube URL  
- 🧠 Extracts transcript (Hindi + English fallback)  
- ✍️ Generates **professional blog-style article**  
- 🌐 Converts article into:
  - HTML  
  - CSS  
  - JavaScript  
- 📦 Download ready-to-use **website ZIP**  
- ⚡ Handles **long videos using recursive summarization**

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- LangChain  
- Google Gemini (`langchain_google_genai`)  
- YouTube Transcript API  
- dotenv  

---


---

How It Works
🔹 1. Transcript Extraction
Uses YouTube transcript loader
Supports:
Hindi (hi)
English (en) fallback
🔹 2. Smart Summarization
✅ Short Videos
Direct summarization using LLM
✅ Long Videos
Splits transcript into chunks
Uses recursive summarization
Maintains running summary
🔹 3. Article Generation
Removes:
Ads
Promotions
Intro noise
Converts into:
Clean blog-style article
Structured content
🔹 4. Website Generation

AI generates structured output in this format:

--html--
--css--
--js--
🔹 5. File Creation

Automatically creates:

index.html
style.css
script.js

And packages them into:

website.zip
💻 UI (Streamlit)
Input: YouTube URL
Output:
HTML tab
CSS tab
JS tab
Download full website
❗ Common Issues
🔴 Streamlit Error

Error:
Streamlit requires raw Python (.py) files

Fix:
Make sure your file has .py extension:

streamlit run app.py

.

🙌 Author

Hruthik
