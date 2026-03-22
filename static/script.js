const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const resultsSection = document.getElementById('results');
const errorDiv = document.getElementById('error');

// Drag and drop functionality
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

// File input change event
fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect() {
    const file = fileInput.files[0];
    if (file && file.type === 'application/pdf') {
        document.getElementById('fileName').textContent = `✓ ${file.name}`;
        analyzeResume(file);
    } else {
        showError('Please select a valid PDF file');
        fileInput.value = '';
    }
}

function analyzeResume(file) {
    const formData = new FormData();
    formData.append('file', file);

    // Show loading state
    const originalContent = uploadBox.innerHTML;
    uploadBox.innerHTML = '<div class="loading"></div><p>Analyzing your resume...</p>';

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
            uploadBox.innerHTML = originalContent;
        } else {
            displayResults(data);
        }
    })
    .catch(error => {
        showError('Error analyzing resume: ' + error.message);
        uploadBox.innerHTML = originalContent;
    });
}

function displayResults(data) {
    const resultsSection = document.getElementById('results');
    
    // Update score
    const scoreValue = document.getElementById('scoreValue');
    scoreValue.textContent = Math.round(data.score);
    
    // Animate progress ring
    const circle = document.querySelector('.progress-ring-circle');
    const radius = circle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (data.score / 100) * circumference;
    
    circle.style.strokeDashoffset = offset;
    circle.classList.add('filled');
    
    // Update message
    document.getElementById('scoreMessage').textContent = data.message;
    
    // Display skills
    const skillsList = document.getElementById('skillsList');
    if (data.skills.length > 0) {
        skillsList.innerHTML = data.skills.map(skill => 
            `<div class="skill-tag">${skill.charAt(0).toUpperCase() + skill.slice(1)}</div>`
        ).join('');
    } else {
        skillsList.innerHTML = '<div class="empty-skills">No recognized skills found in resume</div>';
    }
    
    // Hide error and show results
    errorDiv.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    resultsSection.classList.add('hidden');
}

function resetAnalyzer() {
    fileInput.value = '';
    document.getElementById('fileName').textContent = '';
    resultsSection.classList.add('hidden');
    errorDiv.classList.add('hidden');
    uploadBox.innerHTML = `
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
        </svg>
        <h2>Upload Your Resume</h2>
        <p>Drag and drop your PDF or click to browse</p>
        <input type="file" id="fileInput" accept=".pdf" hidden>
        <button class="btn-primary" onclick="document.getElementById('fileInput').click()">
            Choose File
        </button>
        <p class="file-info" id="fileName"></p>
    `;
    
    // Re-attach event listener to new file input
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);
    uploadBox.scrollIntoView({ behavior: 'smooth' });
}

// Click on upload box to trigger file input
uploadBox.addEventListener('click', function(e) {
    if (e.target !== fileInput) {
        fileInput.click();
    }
});
