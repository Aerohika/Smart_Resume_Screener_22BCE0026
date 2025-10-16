import os
import time
import sqlite3
import re
from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF
from google import genai
from dotenv import load_dotenv

# -----------------------------
# CONFIGURATION
# -----------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["DB_FILE"] = "resumes.db"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------
# DATABASE SETUP
# -----------------------------
def init_db():
    conn = sqlite3.connect(app.config["DB_FILE"])
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            match_score INTEGER,
            summary TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_result_to_db(filename, score, summary):
    conn = sqlite3.connect(app.config["DB_FILE"])
    c = conn.cursor()
    c.execute("""
        INSERT INTO results (filename, match_score, summary)
        VALUES (?, ?, ?)
    """, (filename, score, summary))
    conn.commit()
    conn.close()

def fetch_all_results():
    conn = sqlite3.connect(app.config["DB_FILE"])
    c = conn.cursor()
    c.execute("SELECT filename, match_score, summary FROM results ORDER BY match_score DESC")
    data = c.fetchall()
    conn.close()
    return data

# -----------------------------
# HELPER: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text.strip()

# -----------------------------
# HELPER: Gemini call with retry
# -----------------------------
def generate_with_retry(prompt_text, model_name, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_text
            )
            return response.candidates[0].content.parts[0].text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
            raise e

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    job_desc = request.form.get("jobdesc")
    files = request.files.getlist("resumes")

    if not job_desc or not files:
        return jsonify({"error": "Please upload resumes and add a job description."})

    results_list = []

    for file in files:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        resume_text = extract_text_from_pdf(file_path)

        prompt = f"""
You are an expert HR assistant.
Compare the following resume with the job description and provide this structured output:

1. Match percentage (1–100)
2. Key strengths
3. Missing or weak skills
4. Suggestions for improvement
5. One-line summary of fit

--- Resume ---
{resume_text}

--- Job Description ---
{job_desc}
"""

        try:
            try:
                result = generate_with_retry(prompt, "models/gemini-2.5-pro")
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    result = generate_with_retry(prompt, "models/gemini-2.5-flash")
                else:
                    raise e
        except Exception as e:
            result = f"Error: {str(e)}"

        # -----------------------------
        # Extract match score safely using regex
        # -----------------------------
        match = re.search(r"Match percentage[:\s]*([0-9]{1,3})\s*%", result, re.IGNORECASE)
        if match:
            score = int(match.group(1))
        else:
            score = 0

        # Save to DB (full summary, not truncated)
        save_result_to_db(file.filename, score, result)

        results_list.append({
            "filename": file.filename,
            "score": score,
            "summary": result
        })

    return jsonify({"results": results_list})

@app.route("/history", methods=["GET"])
def history():
    """Return all past results from the database."""
    data = fetch_all_results()
    results = [{"filename": r[0], "score": r[1], "summary": r[2]} for r in data]
    return jsonify({"results": results})

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    init_db()
    app.run(debug=True)
