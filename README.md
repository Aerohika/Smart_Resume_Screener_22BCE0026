# Smart Resume Screener - 22BCE0026
Demo Video: https://drive.google.com/file/d/13EK3JBL4eBQK0Bthr-dgy_jmRF9e__fh/view?usp=drivesdk
A Flask-based web application that intelligently analyzes resumes against a job description using Google's Gemini AI (LLM). The app extracts text from uploaded PDFs and generates a structured report highlighting match percentage, key strengths, missing skills, and suggestions for improvement.

---

## Architecture
--- 

The Smart Resume Screener follows this workflow:

1. **User Interaction**
   - User uploads their **Resume** and **Job Description** via the web interface.

2. **Flask Web App (`app.py`)**
   - Handles file uploads.
   - Extracts text from PDFs using **PyMuPDF**.

3. **Gemini AI (LLM)**
   - Analyzes the extracted text.
   - Compares resume with job description.
   - Identifies key strengths, missing skills, and improvement suggestions.

4. **Structured JSON Response**
   - Stores the analysis in a structured format for easy processing.

5. **Frontend Display**
   - **HTML + JavaScript** renders the results.
   - Shows match percentage, key strengths, missing skills, and suggestions to the user.

**Flow Diagram**

```plaintext
User
 │
 ▼
Uploads Resume & Job Description
 │
 ▼
Flask Web App (PDF Text Extraction)
 │
 ▼
Gemini AI (Resume Analysis)
 │
 ▼
Structured JSON Response
 │
 ▼
Frontend (HTML + JS) → Displays Analysis to User


---
## LLM Prompts

You are an intelligent HR assistant.
Compare the following resume with the given job description and provide a structured, professional analysis:

Match percentage (1–100%)

Key strengths and relevant experience

Missing or weak skills

Suggestions for improvement (keywords, tools, certifications)

One-line summary: Is this candidate a strong fit?

--- Resume ---
<Extracted resume text>

--- Job Description ---
<Provided job description>

---

## How to Run

# Clone the repository
git clone https://github.com/Aerohika/Smart_Resume_Screener_22BCE0026.git
cd Smart_Resume_Screener_22BCE0026

# Create a virtual environment and activate it
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
GEMINI_API_KEY=your_api_key_here

# Run the app
python app.py

# Open in browser
http://127.0.0.1:5000/
Folder Structure
smart-resume-screener/
│
├── app.py                 # Main Flask app
├── requirements.txt       # Dependencies
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── .gitignore             # Ignore uploads, .env
└── README.md              # Project documentation
Features
Extracts text from resumes in PDF format using PyMuPDF.

Analyzes resumes against job descriptions using Gemini AI LLM.

Generates a structured report including:

Match percentage

Key strengths

Missing or weak skills

Suggestions for improvement

One-line candidate fit summary

User-friendly web interface built with Flask, HTML, and JavaScript.

Technologies Used
Python, Flask

PyMuPDF (for PDF text extraction)

HTML, CSS, JavaScript (Frontend)

Gemini AI LLM (Resume analysis)

dotenv (Environment variable management)

