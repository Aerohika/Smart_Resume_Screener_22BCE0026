import os
import time
from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF for PDF text extraction
from google import genai  # Gemini SDK
from dotenv import load_dotenv  # For loading environment variables

# -----------------------------
# CONFIGURATION
# -----------------------------

# Load environment variables from .env
load_dotenv()

# Fetch the Gemini API key securely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please create a .env file and add your key.")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------
# HELPER FUNCTION: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(file_path):
    """Extracts text from a PDF using PyMuPDF."""
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text.strip()

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """Analyze resume vs job description using Gemini with retry and fallback."""
    job_desc = request.form.get("jobdesc")
    file = request.files.get("resume")

    if not job_desc or not file:
        return jsonify({"result": " Please upload a resume and paste a job description."})

    # Save uploaded file
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_path)

    # Gemini prompt
    prompt = f"""
You are an intelligent HR assistant.
Compare the following resume with the given job description and provide a structured, professional analysis:

1️⃣ Match percentage (1–100%)
2️⃣ Key strengths and relevant experience
3️⃣ Missing or weak skills
4️⃣ Suggestions for improvement (keywords, tools, certifications)
5️⃣ One-line summary: Is this candidate a strong fit?

--- Resume ---
{resume_text}

--- Job Description ---
{job_desc}
"""

    # -----------------------------
    # SMART MODEL HANDLING
    # -----------------------------
    def generate_with_retry(prompt_text, model_name, retries=3, delay=2):
        """Retries Gemini call a few times if the model is overloaded."""
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_text
                )
                # Use correct property
                return response.candidates[0].content.parts[0].text
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    if attempt < retries - 1:
                        time.sleep(delay)
                        continue  # retry again
                raise e  # if it's another error, stop retrying

    try:
        # Try Gemini 2.5 Pro first
        try:
            result = generate_with_retry(prompt, "models/gemini-2.5-pro")
        except Exception as e:
            # Fallback to Flash model if Pro fails
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                result = generate_with_retry(prompt, "models/gemini-2.5-flash")
            else:
                raise e

    except Exception as e:
        result = f"Error: {str(e)}"

    return jsonify({"result": result})

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
