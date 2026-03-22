# AI Resume Analyzer

A modern web application that analyzes resumes, detects skills, and calculates ATS (Applicant Tracking System) scores.

## Features

- 📄 **PDF Resume Upload** - Drag and drop or browse to upload your resume
- 🎯 **Skill Detection** - Automatically detects relevant skills from your resume
- 📊 **ATS Score** - Gets an instant ATS score out of 100%
- 🎨 **Modern UI** - Beautiful, responsive HTML/CSS frontend
- ⚡ **Fast Processing** - Quick analysis and instant results

## Project Structure

```
resume-analyzer/
├── app.py                 # Flask backend server
├── resume_parser.py       # PDF text extraction
├── skill.py              # Skill detection logic
├── scorer.py             # ATS score calculation
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Main frontend page
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend logic
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd resume-analyzer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Navigate to `http://localhost:5000`

3. **Upload a resume:**
   - Drag and drop your PDF resume or click to browse
   - The app will analyze it and show results instantly

## Detected Skills

The analyzer looks for these skills in your resume:
- Python
- Java
- SQL
- Machine Learning
- Data Analysis
- Excel
- Power BI
- Tableau

## How It Works

1. **PDF Extraction** - Extracts all text from the uploaded PDF
2. **Skill Matching** - Searches for predefined skills in the extracted text
3. **Score Calculation** - Calculates ATS score based on found skills (max 8 skills = 100%)
4. **Results Display** - Shows detected skills and ATS score with recommendations

## Customization

To add more skills to detect, edit `skill.py`:

```python
skills_list = [
    "python", "java", "sql", "machine learning",
    "data analysis", "excel", "power bi", "tableau"
    # Add more skills here
]
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **PDF Processing:** pdfplumber
- **Server:** Werkzeug

## Notes

- Maximum file size: 16MB
- Only PDF files are accepted
- Resume text is analyzed in lowercase for case-insensitive matching
- Results are shown instantly without page reload

## License

This project is open source and available under the MIT License.
