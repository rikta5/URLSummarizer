# URL Summarizer API

## 📌 Project Overview
The **URL Summarizer API** is a web application that extracts text from a given URL and generates a concise summary. It supports multiple languages, allows users to control summary length, and features a dark mode for a better reading experience.

## 🚀 Features
- **Extracts text** from articles and webpages.
- **Summarizes content** into 1-10 sentences.
- **Supports multiple languages**.
- **Dark Mode toggle** for user preference.
- **Caching** for improved performance.
- **Responsive UI**.

## 🛠️ Tech Stack
- **Backend:** Flask (Python), Newspaper3k, Sumy (LexRank Summarizer)
- **Frontend:** HTML, CSS, JavaScript
- **Caching:** Flask-Caching

## 📥 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/rikta5/url-summarizer.git
cd url-summarizer
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

### 3️⃣ Run the Flask App
```bash
python app.py
```
**Open in Browser:** `http://127.0.0.1:5000/`

## 🔧 How It Works
1. Enter a **URL** in the input field.
2. Select the **number of sentences** for the summary.
3. Click **"Summarize"** to fetch and display the summary.
4. Toggle **Dark Mode** for a better reading experience.

