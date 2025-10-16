# Smart Resume Screener - 22BCE0026
Demo Video: https://drive.google.com/file/d/1SADvj-eGlaOu-QGjJZQu4FbYFn6mnV0F/view?usp=drivesdk

A Flask-based web application that intelligently analyzes resumes against a job description using Google's Gemini AI (LLM). The app extracts text from uploaded PDFs and generates a structured report highlighting match percentage, key strengths, missing skills, and suggestions for improvement.

---

## Architecture
--- 
The Smart Resume Screener follows a modular workflow to analyze resumes against job descriptions and provide actionable insights:
1.	User Interaction
   o	Users upload their Resume and Job Description via the web interface.
2.	Flask Web App (app.py)
   o	Handles file uploads securely and manages temporary storage.
   o	Extracts text from uploaded PDFs using PyMuPDF.
3.	Gemini AI (LLM) Analysis
   o	Analyzes the extracted resume and job description.
   o	Compares the resume against job requirements.
   o	Identifies key strengths, missing or weak skills, and provides suggestions for improvement.
4.	Structured JSON Response
   o	Stores the LLM analysis in a structured JSON format for easy processing and frontend display.
   o	Includes: match percentage, key strengths, missing skills, suggestions, and a one-line summary.
5.	Frontend Display
   o	Uses HTML + JavaScript to dynamically render results to the user.
   o	Displays the match percentage, key strengths, missing skills, and suggestions clearly and concisely.


**Flow Diagram**

```plaintext
User
  │
  ▼
Uploads Resume & Job Description
  │
  ▼
Flask Web App (app.py)
  │
  ├─ PDF Text Extraction (PyMuPDF)
  │
  ├─ Gemini AI (LLM)
  │    └─ Compares resume with job description
  │
  └─ Structured JSON Response
       ├─ Match Percentage
       ├─ Key Strengths
       ├─ Missing/Weak Skills
       ├─ Suggestions
       └─ One-Line Summary
  │
  ▼
Frontend (HTML + JS)
  └─ Displays analysis results to the user
  │
  ▼
SQLite Database (resumes.db)
  └─ Stores history of analyses (filename, match score, summary)



---
## LLM Prompts

You are an expert HR assistant.
Compare the following resume with the job description and provide this structured output:

1. Match percentage (1–100)
2. Key strengths
3. Missing or weak skills
4. Suggestions for improvement
5. One-line summary of fit

--- Resume ---
<INSERT_RESUME_TEXT_HERE>

--- Job Description ---
<INSERT_JOB_DESCRIPTION_HERE>

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
•	Flask – Handles web server, routing, and API endpoints.
•	PyMuPDF (fitz) – Extracts text from uploaded PDF resumes.
•	Google Gemini AI (genai) – Performs resume analysis and comparison with job descriptions.
•	sqlite3 – Stores analysis results (filename, match score, summary).
•	dotenv (python-dotenv) – Loads environment variables like GEMINI_API_KEY.
•	os & time – File management, folder creation, and retry delays.
•	re – Extracts numeric match percentage reliably from LLM output

