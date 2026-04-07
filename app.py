"""
AI Resume Analyzer - Flask Application

A comprehensive resume analysis tool that provides ATS scoring, keyword matching,
skill alignment analysis, and actionable recommendations using advanced multi-factor
algorithms. This application helps job seekers optimize their resumes for applicant
tracking systems and improve their chances of interview callbacks.

Features:
    - 6-factor weighted ATS scoring system (0-100)
    - Job description matching and alignment analysis
    - Keyword extraction and gap identification
    - Skill taxonomy alignment with ATS requirements
    - Seniority level matching
    - Educational credential scoring
    - Professional experience assessment
    - Actionable improvement recommendations
    - Real-time processing with detailed feedback

Author: Resume Analyzer Team
License: MIT
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text
from ats_scorer import calculate_ats_score, extract_keywords_from_jd
from skill import extract_skill, skills_list
import os
import logging
from typing import Dict, Tuple, Any

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
    logger.info(f"Created uploads folder at {os.path.abspath('uploads')}")


@app.route('/')
def index():
    """
    Serve the main application page
    
    Returns:
        HTML template for the resume analyzer
    """
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return jsonify({'error': 'Failed to load application'}), 500


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze uploaded resume using comprehensive ATS scoring.
    
    Expected Form Data:
        - file: PDF file to analyze (required)
        - job_description: Job description text (optional)
    
    Returns:
        JSON response with:
        - ats_score: Overall ATS match score (0-100)
        - grade: Letter grade (A-F)
        - classification: Human-readable classification
        - factors: Breakdown of each scoring factor
        - missing_keywords: Top keywords missing from resume
        - strengths: Top detected strengths
        - suggestions: Actionable suggestions for each weak area
        - warnings: Any warnings about resume quality
        - skills: Legacy skill detection (for backward compatibility)
        - message: Human-readable feedback
    """
    try:
        # Validate file is present
        if 'file' not in request.files:
            logger.warning('Analysis request received without file')
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        job_description = request.form.get('job_description', '').strip()
        
        # Validate filename
        if file.filename == '':
            logger.warning('Analysis request received with empty filename')
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file extension
        if not file.filename.lower().endswith('.pdf'):
            logger.warning(f'Invalid file type attempted: {file.filename}')
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Extract text from PDF
        logger.info(f"Analyzing resume: {file.filename}")
        resume_text = extract_text(file)
        
        if not resume_text or not resume_text.strip():
            logger.warning(f"No text extracted from: {file.filename}")
            return jsonify({'error': 'Could not extract text from PDF. Please ensure the PDF is not empty or scanned.'}), 400
        
        # Legacy: Extract skills using original method
        legacy_skills = extract_skill(resume_text)
        
        # NEW: Calculate comprehensive ATS score
        ats_result = calculate_ats_score(
            resume_text,
            job_description if job_description else None,
            debug=False
        )
        
        logger.info(
            f"Analysis complete for {file.filename}: "
            f"ATS Score={ats_result.total_score:.1f}, "
            f"Grade={ats_result.grade}, "
            f"Skills={len(legacy_skills)}"
        )
        
        # Build response combining legacy and new scoring
        response = {
            # New comprehensive ATS scoring
            'ats_score': ats_result.total_score,
            'ats_grade': ats_result.grade,
            'ats_classification': ats_result.classification,
            'ats_factors': [f.to_dict() for f in ats_result.factor_scores],
            'missing_keywords': ats_result.missing_keywords,
            'strengths': ats_result.strengths,
            'suggestions': ats_result.suggestions,
            'warnings': ats_result.warnings,
            
            # Legacy data for backward compatibility
            'skills': legacy_skills,
            'score': ats_result.total_score,  # Use ATS score as main score
            'total_skills': len(skills_list),
            'message': ats_result.classification
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"Validation error during analysis: {str(e)}")
        return jsonify({'error': f'Invalid file: {str(e)}'}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while analyzing the resume. Please try again.'}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size limit exceeded"""
    logger.warning(f"File upload exceeded size limit")
    return jsonify({'error': 'File size exceeds 16MB limit. Please select a smaller file.'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return jsonify({'error': 'An internal server error occurred. Please try again later.'}), 500


if __name__ == '__main__':
    logger.info("Starting AI Resume Analyzer with Advanced ATS Scoring")
    app.run(debug=True)