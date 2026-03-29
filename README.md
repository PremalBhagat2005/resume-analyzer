# AI Resume Analyzer

A resume analyzer that actually tells you how well your resume stacks up against job descriptions. Upload a resume, optionally paste a job description, and get a detailed breakdown of your ATS score plus actionable feedback.

## What It Does

- ATS Score out of 100 based on 6 factors that ATS systems actually care about
- Paste a job description to see how well your resume aligns with what employers want
- See exactly what's contributing to your score: keywords, skills, seniority, education, experience, and formatting
- Find out what key terms from the job description are missing in your resume
- Get specific recommendations to improve weak areas
- Dark/light mode toggle, smooth animations, doesn't look clunky
- Results show up instantly

## How to Run It

First time:
```bash
cd resume-analyzer
pip install -r requirements.txt
```

Then:
```bash
python app.py
```

Open `http://localhost:5000` and upload a PDF resume.

## The ATS Scoring System

Your score comes from:
- Keyword Match (30%) - Does your resume have relevant terms from the job description?
- Skills Alignment (25%) - Do you have the technical skills they're asking for?
- Seniority Level (15%) - Do your years of experience match the role?
- Education (10%) - Degrees, certifications, etc.
- Experience (10%) - Job titles, companies, years in field
- Formatting (10%) - Clean structure, proper formatting

Without a job description, you still get 8-12% for having a properly formatted resume with content.

## What's in Here

```
resume-analyzer/
├── app.py              # Flask backend
├── ats_scorer.py       # The 6-factor scoring
├── resume_parser.py    # Extracts text from PDFs
├── skill.py            # Skill detection
├── scorer.py           # Legacy scoring
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Main page
└── static/
    ├── script.js       # Frontend stuff
    └── style.css       # Styling + animations
```

**ats_scorer.py** does the heavy lifting:
- Extracts keywords from resume and job description
- Matches skills against a hardcoded list
- Detects seniority from keywords like "senior", "lead", "junior"
- Checks for education keywords
- Looks at work experience patterns
- Evaluates formatting quality

Keyword match gets the highest weight because that's what ATS actually cares about most.

**Frontend** is vanilla JavaScript (no frameworks):
- Uploads PDFs and gets JSON results back
- Renders the circular progress ring that animates to your score
- Shows all 6 factors with color-coded ratings
- Lists missing keywords by priority
- Provides suggestions organized by category
- Dark/light mode toggle

## Detected Skills

The system looks for 50+ hard skills across these categories:
- Languages: Python, Java, C++, JavaScript, etc.
- Data: SQL, Excel, Tableau, Power BI, etc.
- Big data: Spark, Hadoop, etc.
- Cloud: AWS, Azure, GCP
- ML frameworks: TensorFlow, PyTorch, Scikit-learn
- Plus soft skills: leadership, communication, project management, etc.

## File Upload

- PDF only
- No size limit enforced (Python's pdfplumber will handle it)
- Text gets extracted and analyzed

## Notes

- Results update in real-time without page reload
- Your data stays in the browser - nothing is saved server-side
- The job description is optional, but you'll get better feedback if you include it
- Scores are normalized to 0-100, with a minimum floor of 8% for any valid resume

## Browser Compatibility

Works on any modern browser - Chrome, Firefox, Safari, Edge. The animations might be slightly smoother on newer versions but nothing fancy that would break on older browsers.
