from flask import Flask, render_template, request, jsonify
from resume_parser import extract_text
from skill import extract_skill
from scorer import calculate_score
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        text = extract_text(file)
        skills = extract_skill(text)
        score = calculate_score(skills)
        
        return jsonify({
            'skills': skills,
            'score': score,
            'total_skills': 8,
            'message': '⚠️ Improve your resume by adding more relevant skills!' if score < 50 else '✅ Great resume! Keep it up!'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)