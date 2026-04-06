# AI Resume Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.3+](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)

A resume analyzer that actually tells you how well your resume stacks up against job descriptions. Upload a resume, optionally paste a job description, and get a detailed breakdown of your ATS score plus actionable feedback.

## Features

- **ATS Score (0-100)** - Comprehensive scoring based on 6 factors that ATS systems actually care about
- **Job Description Matching** - Paste a job description to see how well your resume aligns
- **Factor Breakdown** - Detailed view of: keywords, skills, seniority, education, experience, and formatting
- **Missing Keywords** - See exactly what terms from the job description are missing in your resume
- **Actionable Recommendations** - Get specific suggestions to improve weak areas
- **Dark/Light Mode** - Smooth theme toggle with persistent preferences
- **Real-time Results** - Instant analysis without page reload
- **Privacy First** - No data saved server-side, all processing is local-first

## What It Does

- ATS Score out of 100 based on 6 factors that ATS systems actually care about
- Paste a job description to see how well your resume aligns with what employers want
- See exactly what's contributing to your score: keywords, skills, seniority, education, experience, and formatting
- Find out what key terms from the job description are missing in your resume
- Get specific recommendations to improve weak areas
- Dark/light mode toggle, smooth animations, doesn't look clunky
- Results show up instantly

## Quick Start

### Requirements
- Python 3.8+
- pip (Python package manager)

### Installation

**First time setup:**
```bash
# Clone the repository
git clone <repository-url>
cd resume-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

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

Your score comes from 6 weighted factors (total = 100%):

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Keyword Match** | 30% | Does your resume have relevant terms from the job description? |
| **Skills Alignment** | 25% | Do you have the technical skills they're asking for? |
| **Seniority Level** | 15% | Do your years of experience match the role? |
| **Education** | 10% | Degrees, certifications, and academic qualifications |
| **Experience** | 10% | Job titles, companies, years in field, career progression |
| **Formatting** | 10% | Clean structure, proper formatting, readability |
Project Structure

```
resume-analyzer/
├── app.py                    # Flask backend - main application entry point
├── ats_scorer.py             # Core ATS scoring engine (6-factor system)
├── resume_parser.py          # PDF extraction and text processing
├── skill.py                  # Technical skill detection and categorization
├── scorer.py                 # Legacy scoring module (maintained for compatibility)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── templates/
│   └── index.html            # Main web interface (responsive design)
│
├── static/
│   ├── script.js             # Frontend JavaScript (vanilla, no frameworks)
│   └── style.css             # Styling with animations and dark mode
│
└── uploads/                  # Temporary storage for uploaded PDFs
```

### Key Components

#### Backend (`app.py`)
- Flask micro-framework for HTTP server
- Route: `POST /analyze` - processes resume uploads
- Route: `GET /` - serves main HTML page
- Error handling and logging
- File upload validation and security

#### ATS Scoring Engine (`ats_scorer.py`)
- **6-factor weighted scoring system**
- Keyword extraction from job descriptions
- Skills matching against curated technology list
- Seniority level detection from experience keywords
- Education verification (degree, certification detection)
- Experience scoring (years, promotions, job titles)
- Formatting quality assessment
- Detailed feedback generation
- Actionable suggestions by category

#### Resume Processing (`resume_parser.py`)
- Robust PDF text extraction using pdfplumber
- Handles encrypted and damaged PDFs gracefully
- Multi-page processing with page-level error recovery
- Text normalizati & Technologies

The system recognizes 50+ technical skills and frameworks across these categories:

### Programming Languages
Python, Java, JavaScript, TypeScript, C++, C#, PHP, Ruby, Go, Rust, Kotlin, Scala, R, Swift, Objective-C, Perl, MATLAB

### Web Technologies & Frameworks
HTML, CSS, React, Angular, Vue.js, Node.js, Express, Django, Flask, ASP.NET, Ruby on Rails, Spring, Laravel, FastAPI

###Supported File Formats

- **Resume**: PDF only (with robust error handling)
- **Job Description**: Paste as plain text
- **No size limits** enforced on resume processing

## Usage Tips

### For Best Results:

1. **Include a Job Description** - The more context provided, the better the score accuracy
2. **Use Standard Resume Format** - Clear sections (Experience, Skills, Education, etc.)
3. **Include Relevant Keywords** - Mirror job description terminology where applicable
4. **List Technical Skills** - Create a dedicated "Skills" section
5. **Add Certifications** - Include relevant professional certifications
6. **Quantify Experience** - Years of experience in specific areas

### Example Workflow:

1. Copy job description from job posting
2. Paste into "Job Description" field
3. Upload your PDF resume
4. Review ATS score and factors
5. Check "Missing Keywords" section
6. Implement suggestions to improve score
7. Re-upload updated resume to compare

## API Documentation

### POST `/analyze`

Analyzes a resume against an optional job description.

**Request:**
- `Development

### Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Debug Mode
Fully compatible with all modern browsers:
- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

The animations and transitions work smoothly on newer versions. Older browsers will still function but may have slightly different visual presentation.

## Performance

- Average analysis time: 200-500ms
- Supports resumes up to 16MB
- Can handle multi-page PDFs efficiently
- Responsive UI with no blocking operations

## License

This project is open source. See LICENSE file for details.

## Future Enhancements

Planned features and improvements:
- [ ] Support for DOCX and TXT resume formats
- [ ] Industry-specific scoring profiles
- [ ] Resume improvement recommendations
- [ ] Batch processing for multiple resumes
- [ ] Export results as PDF
- [ ] Resume versioning and comparison
- [ ] Integration with LinkedIn profiles
- [ ] Grammar and readability analysis
- [ ] Salary expectation based on profile

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests. See CONTRIBUTING.md for guidelines.

## Support & Feedback

- Found a bug? Open an issue
- Have a suggestion? Create a feature request
- Questions? Check existing issues or documentation

## Changelog

### Version 1.0.0
- Initial release with 6-factor ATS scoring
- PDF resume parsing and analysis
- 50+ skill detection
- Dark/light mode toggle
- Real-time analysis results

---

**Made with ❤️ to help you get your resume past ATS systems**
The application includes Flask debug mode for development:
- Automatic server reload on code changes
- Interactive debugger for exceptions
- Request/response logging

### Testing Your Changes

1. Upload a sample resume (PDF)
2. Test with and without job description
3. Verify ATS score calculation
4. Check factor breakdown accuracy
5. Review console logs for errors

## Troubleshooting

### Application Won't Start
- Ensure Python 3.8+ is installed: `python --version`
- Check all dependencies: `pip list`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

### PDF Upload Fails
- Ensure file is valid PDF format
- Try a different PDF if upload persists
- Check browser console for error messages
- Verify file is not corrupted

### Incorrect ATS Score
- Include job description for accurate scoring
- Ensure resume text is properly extracted
- Check that skills are spelled correctly
- Verify resume has clear sections

### Slow Performance
- Large PDFs (10+ pages) may take longer
- Try smaller sample resumes first
- Check system memory availability
- Monitor network in browser DevTools

## Notes

- Results update in real-time without page reload
- Your data stays in the browser - nothing is saved server-side
- The job description is optional, but you'll get better feedback if you include it
- Scores are normalized to 0-100, with a minimum floor of 8% for any valid resume
- All processing happens server-side; no third-party APIs are called
**Response (JSON):**
```json
{
  "ats_score": 82.5,
  "ats_grade": "B",
  "ats_classification": "Good",
  "ats_factors": [
    {
      "name": "keyword_match",
      "weight": 0.30,
      "score": 85,
      "max_score": 100,
      "feedback": "Good keyword alignment with job description"
    }
  ],
  "missing_keywords": ["kubernetes", "microservices", "lambda"],
  "strengths": ["Strong Python background", "AWS experience", "Leadership experience"],
  "suggestions": {
    "keyword_match": "Add more specific terminology from job description",
    "skills_alignment": "Highlight Docker and containerization experience"
  },
  "warnings": []
}
```
### Soft Skills
Communication, Leadership, Teamwork, Problem Solving, Project Management, Agile, Scrum, Kanban, Critical Thinking
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

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) guide to get started.

### Quick Contribution Steps:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit changes (`git commit -m 'Add awesome feature'`)
4. Push to branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## 📋 Code of Conduct

Please read our [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) to understand our community standards.

## 💬 Support & Feedback

- Found a bug? [Open an issue](../../issues)
- Have a suggestion? [Create a discussion](../../discussions)
- Want to contribute? Check [CONTRIBUTING.md](./CONTRIBUTING.md)

---

**Made with ❤️ to help you beat ATS systems and land interviews**
