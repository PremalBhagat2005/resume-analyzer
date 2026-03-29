# AI Resume Analyzer

A resume analyzer that actually tells you how well your resume stacks up against job descriptions. Upload a resume, optionally paste a job description, and get a detailed breakdown of your ATS score plus actionable feedback.

## What It Does

- **🎯 ATS Score** - Get a score out of 100 based on 6 factors that ATS systems actually care about
- **📋 Job Description Matching** - Paste a job description to see how well your resume aligns with what employers are looking for
- **📊 Factor Breakdown** - See exactly what's contributing to your score: keywords, skills, seniority, education, experience, and formatting
- **⚠️ Missing Keywords** - Find out what key terms from the job description are missing in your resume
- **💡 Smart Suggestions** - Get specific recommendations to improve each weak area
- **🎨 Modern UI** - Dark/light mode, smooth animations, clean design that doesn't feel clunky
- **⚡ Instant Results** - No waiting around, analysis happens fast

## How to Run It

**First time setup:**
```bash
cd resume-analyzer
pip install -r requirements.txt
```

**Start the app:**
```bash
python app.py
```

Then open `http://localhost:5000` in your browser and upload a PDF resume.

## The ATS Scoring System

Your score is calculated from:
- **Keyword Match (30%)** - Does your resume contain relevant terms from the job description?
- **Skills Alignment (25%)** - Do you have the technical skills being asked for?
- **Seniority Level (15%)** - Do your years of experience match the role's level?
- **Education (10%)** - Relevant degrees, certifications, etc.
- **Experience (10%)** - Job titles, companies, years in field
- **Formatting (10%)** - Clean structure, proper formatting

Even without a job description, you'll get an 8-12% baseline score just for having a properly formatted resume with detectable content.

## What's in the Code

```
resume-analyzer/
├── app.py              # Flask server that ties everything together
├── ats_scorer.py       # The 6-factor scoring engine
├── resume_parser.py    # Extracts text from PDFs
├── skill.py            # Skill detection (Python, Java, SQL, etc.)
├── scorer.py           # Legacy scoring (kept for reference)
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Main page - single page app
└── static/
    ├── script.js       # All the interactive bits
    └── style.css       # Dark mode + animations
```

## Project Structure Details

**ats_scorer.py** - This is the real workhorse. It:
- Extracts keywords from both resume and job description
- Matches skills against hardcoded skill lists
- Detects seniority level from keywords like "senior", "lead", "junior", etc.
- Checks for education keywords (degree types, institution names)
- Looks at work experience patterns
- Evaluates formatting quality

The scoring is weighted so keyword match has the biggest impact (makes sense - that's what ATS cares about most).

**Frontend** - Built with vanilla JavaScript, no frameworks. It:
- Uploads PDFs to Flask and gets back JSON results
- Displays the circular progress ring that animates to your score
- Shows all 6 factors with color-coded ratings
- Lists missing keywords with priority levels
- Provides improvement suggestions organized by category
- Lets you toggle dark/light mode

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
