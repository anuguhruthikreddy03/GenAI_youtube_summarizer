# 📺 YouTube → Article → Website Generator
---

## 🚀 Features

* 🔗 Input YouTube URL
* 🧠 Extracts transcript (Hindi + English fallback)
* ✍️ Generates **professional blog-style article**
* 🌐 Converts article into:

  * HTML
  * CSS
  * JavaScript
* 📦 Download ready-to-use **website ZIP**
* ⚡ Handles **long videos using recursive summarization**

---

## 🛠️ Tech Stack

* 🐍 Python
* ⚡ Streamlit
* 🔗 LangChain
* 🤖 Google Gemini (`langchain_google_genai`)
* 📺 YouTube Transcript API
* 🔐 dotenv

---

## ⚙️ How It Works

* 📥 Extracts transcript using YouTube Transcript API
* 🌐 Supports Hindi (`hi`) and English (`en`) fallback
* ✂️ Splits long transcripts into smaller chunks
* 🔁 Applies recursive summarization for long videos
* 🧠 Maintains context-aware summaries
* 🧹 Removes ads, promotions, and intro noise
* ✍️ Converts content into structured blog-style article
* 🌐 Generates website code in:

  * HTML
  * CSS
  * JavaScript

---

## 📦 Output Format

* 🤖 AI generates structured response:

  * `--html--`
  * `--css--`
  * `--js--`

---

## 📁 File Generation

* 📄 Creates:

  * `index.html`
  * `style.css`
  * `script.js`
* 📦 Packages all files into:

  * `website.zip`

---

## 💻 UI (Streamlit)

* 🔗 Input:

  * YouTube URL
* 📤 Output:

  * HTML tab
  * CSS tab
  * JavaScript tab
  * Download full website ZIP

---

## ▶️ How to Run

* 📥 Clone the repository
* 📂 Navigate to project folder
* 📦 Install dependencies
* ▶️ Run Streamlit app

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Environment Variables

* 📄 Create `.env` file
* 🔑 Add your API key

```env
GOOGLE_API_KEY=your_api_key_here
```


## 🙌 Author

* 👨‍💻 Hruthik

---

## ⭐ Support

* ⭐ Give this project a star if you like it
