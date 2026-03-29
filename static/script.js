// ============================================================================
// STATE MANAGEMENT
// ============================================================================
const appState = {
    currentAbortController: null,
    isAnalyzing: false,
    analysisStartTime: null
};

// ============================================================================
// DOM ELEMENTS & INITIALIZATION
// ============================================================================
const uploadBox = document.getElementById('uploadBox');
const resultsSection = document.getElementById('results');
const errorDiv = document.getElementById('error');
const themeToggle = document.getElementById('themeToggle');

/**
 * Initialize theme from localStorage and set up theme toggle listener
 */
function initializeTheme() {
    try {
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-mode');
        }

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
        });
    } catch (error) {
        console.error('Error initializing theme:', error);
    }
}

initializeTheme();

// ============================================================================
// FILE INPUT MANAGEMENT
// ============================================================================

/**
 * Get file input element (used to avoid stale closures)
 */
function getFileInput() {
    return document.getElementById('fileInput');
}

/**
 * Attach change event listener to file input
 */
function attachFileInputListener() {
    try {
        const fileInput = getFileInput();
        if (fileInput) {
            fileInput.removeEventListener('change', handleFileSelect);
            fileInput.addEventListener('change', handleFileSelect);
        }
    } catch (error) {
        console.error('Error attaching file input listener:', error);
        showError('Error initializing file upload. Please refresh the page.');
    }
}

/**
 * Attach click handler to choose file button
 */
function attachChooseFileBtnListener() {
    try {
        const chooseFileBtn = document.getElementById('chooseFileBtn');
        if (chooseFileBtn) {
            chooseFileBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const fileInput = getFileInput();
                if (fileInput && !appState.isAnalyzing) {
                    fileInput.click();
                }
            });
        }
    } catch (error) {
        console.error('Error attaching choose file button listener:', error);
    }
}

/**
 * Validate and process selected PDF file
 */
function handleFileSelect() {
    try {
        const fileInput = getFileInput();
        const file = fileInput.files[0];

        if (!file) {
            return;
        }

        // Validate file type
        if (file.type !== 'application/pdf') {
            showError('⚠️ Please select a valid PDF file');
            fileInput.value = '';
            return;
        }

        // Validate file size (max 16MB as per Flask config)
        const MAX_SIZE = 16 * 1024 * 1024;
        if (file.size > MAX_SIZE) {
            showError('⚠️ File size exceeds 16MB limit. Please select a smaller file.');
            fileInput.value = '';
            return;
        }

        // Update UI to show selected file
        document.getElementById('fileName').textContent = `✓ ${file.name}`;
        analyzeResume(file);
    } catch (error) {
        console.error('Error handling file selection:', error);
        showError('❌ Error processing file. Please try again.');
    }
}

// ============================================================================
// DRAG & DROP FUNCTIONALITY
// ============================================================================

/**
 * Setup drag and drop event listeners
 */
function setupDragAndDrop() {
    try {
        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadBox.classList.add('dragover');
        });

        uploadBox.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadBox.classList.remove('dragover');
        });

        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadBox.classList.remove('dragover');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = getFileInput();
                if (fileInput) {
                    fileInput.files = files;
                    handleFileSelect();
                }
            }
        });

        // Prevent default drag behavior on document
        document.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        document.addEventListener('drop', (e) => {
            e.preventDefault();
        });
    } catch (error) {
        console.error('Error setting up drag and drop:', error);
    }
}

setupDragAndDrop();

// ============================================================================
// FILE UPLOAD & ANALYSIS
// ============================================================================

/**
 * Analyze resume by uploading to backend API
 * Uses AbortController to cancel previous requests if new file is selected
 * Includes optional job description for improved ATS scoring
 */
async function analyzeResume(file) {
    try {
        // Cancel any previous analysis request
        if (appState.currentAbortController) {
            appState.currentAbortController.abort();
        }

        // Mark as analyzing
        appState.isAnalyzing = true;
        appState.analysisStartTime = Date.now();

        // Create new abort controller for this request
        appState.currentAbortController = new AbortController();

        // Show loading state
        const originalContent = uploadBox.innerHTML;
        uploadBox.innerHTML = `
            <div class="skeleton-loader">
                <div class="skeleton-line"></div>
                <div class="skeleton-line" style="width: 80%;"></div>
            </div>
            <p class="loading-text">🔍 Analyzing your resume...</p>
        `;

        // Prepare form data
        const formData = new FormData();
        formData.append('file', file);
        
        // Add job description if provided
        const jobDescription = document.getElementById('jobDescription');
        if (jobDescription && jobDescription.value.trim()) {
            formData.append('job_description', jobDescription.value.trim());
        }

        // Send request with abort signal
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
            signal: appState.currentAbortController.signal
        });

        // Check if request was aborted
        if (!response.ok && response.status !== 0) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Check for analysis error
        if (data.error) {
            showError(`❌ ${data.error}`);
            uploadBox.innerHTML = originalContent;
        } else {
            displayResults(data);
        }
    } catch (error) {
        // Don't show error if request was aborted (user cancelled)
        if (error.name === 'AbortError') {
            console.log('Analysis request was cancelled');
            return;
        }

        console.error('Error analyzing resume:', error);
        const errorMessage = error.message || 'Unknown error occurred';
        showError(`❌ Error analyzing resume: ${errorMessage}`);

        // Restore original upload box
        const uploadBox = document.getElementById('uploadBox');
        const fileInput = getFileInput();
        if (uploadBox && fileInput) {
            uploadBox.innerHTML = `
                <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <h2>Upload Your Resume</h2>
                <p>Drag and drop your PDF or click to browse</p>
                <button class="btn-primary" onclick="document.getElementById('fileInput').click(); event.stopPropagation();">
                    Choose File
                </button>
                <p class="file-info" id="fileName"></p>
            `;
            attachFileInputListener();
        }
    } finally {
        appState.isAnalyzing = false;
    }
}

// ============================================================================
// RESULTS DISPLAY
// ============================================================================

/**
 * Helper function to calculate letter grade from numeric score
 */
function getLetterGrade(score) {
    if (score >= 80) return 'A';
    if (score >= 60) return 'B';
    if (score >= 40) return 'C';
    if (score >= 20) return 'D';
    return 'F';
}

/**
 * Helper function to get color based on score
 */
function getScoreColor(score) {
    if (score >= 80) return '#22c55e';  // bright green
    if (score >= 60) return '#3b82f6';  // blue
    if (score >= 40) return '#f59e0b';  // amber
    if (score >= 20) return '#f97316';  // orange
    return '#ef4444';                    // red
}

/**
 * Helper function to get classification text based on score
 */
function getScoreClassification(score) {
    if (score >= 80) return 'Excellent Match';
    if (score >= 60) return 'Good Match';
    if (score >= 40) return 'Fair Match';
    if (score >= 20) return 'Poor Match';
    return 'Poor Match';
}

/**
 * Display analysis results with animations and comprehensive ATS breakdown
 */
function displayResults(data) {
    try {
        // Update score - use ats_score if available, else fall back to score
        const scoreValue = document.getElementById('scoreValue');
        const gradeLetter = document.getElementById('gradeLetter');
        const gradeStatus = document.getElementById('gradeStatus');
        const scoreBadge = document.getElementById('scoreGradeBadge');
        const circle = document.querySelector('.progress-ring-circle');

        if (!scoreValue || !circle) {
            throw new Error('Results elements not found');
        }

        // Determine which score to use
        let finalScore = data.ats_score !== undefined ? data.ats_score : data.score;
        
        // BUG FIX #2: Apply minimum score floor (8-12%)
        // Ensure any parsed resume gets at least 8% credit, 12% if some content exists
        const hasContent = data.ats_factors && data.ats_factors.length > 0;
        finalScore = Math.max(hasContent ? 12 : 8, finalScore);
        
        console.log('[DEBUG] Final ATS Score:', finalScore, 'Original:', data.ats_score);
        
        const grade = data.ats_grade || getLetterGrade(finalScore);
        const classification = data.ats_classification || '';
        const scoreColor = getScoreColor(finalScore);

        // Reset progress ring first and apply color to number
        circle.classList.remove('filled');
        circle.style.stroke = scoreColor;
        scoreValue.style.color = scoreColor;

        // Animate score with counter effect
        animateScoreCounter(0, Math.round(finalScore), 1500);

        // Update badge with grade and classification
        if (gradeLetter) {
            gradeLetter.textContent = grade;
            gradeLetter.style.color = scoreColor;
        }
        if (gradeStatus) {
            gradeStatus.textContent = classification || getScoreClassification(finalScore);
            gradeStatus.style.color = scoreColor;
        }
        if (scoreBadge) {
            scoreBadge.style.borderColor = `${scoreColor}33`;
            scoreBadge.style.backgroundColor = `${scoreColor}11`;
        }

        // Animate progress ring with color
        setTimeout(() => {
            const radius = circle.r.baseVal.value;
            const circumference = radius * 2 * Math.PI;
            const offset = circumference - (finalScore / 100) * circumference;

            circle.style.strokeDashoffset = offset;
            circle.style.filter = `drop-shadow(0 0 8px ${scoreColor})`;
            circle.classList.add('filled');
        }, 100);

        // Update message
        const scoreMessage = document.getElementById('scoreMessage');
        if (scoreMessage) {
            scoreMessage.textContent = data.message || '';
        }

        // Display comprehensive ATS results if available
        if (data.ats_factors) {
            displayFactors(data.ats_factors);
        }

        if (data.strengths) {
            displayStrengths(data.strengths);
        }

        if (data.missing_keywords) {
            displayMissingKeywords(data.missing_keywords);
        }

        if (data.suggestions) {
            displaySuggestions(data.suggestions);
        }

        if (data.warnings && data.warnings.length > 0) {
            displayWarnings(data.warnings);
        }

        // Display skills with staggered animation (backward compatibility)
        if (data.skills) {
            displaySkills(data.skills);
        }

        // Hide error and show results
        errorDiv.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        // Smooth scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    } catch (error) {
        console.error('Error displaying results:', error);
        showError('❌ Error displaying results. Please try again.');
    }
}

/**
 * Animate score counter from 0 to final value
 */
function animateScoreCounter(start, end, duration) {
    try {
        const scoreValue = document.getElementById('scoreValue');
        if (!scoreValue) return;

        const startTime = Date.now();
        const range = end - start;

        function updateScore() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out-quad)
            const easeProgress = 1 - Math.pow(1 - progress, 2);
            const current = Math.floor(start + range * easeProgress);

            scoreValue.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(updateScore);
            }
        }

        updateScore();
    } catch (error) {
        console.error('Error animating score:', error);
        document.getElementById('scoreValue').textContent = end;
    }
}

/**
 * Display detected skills with staggered animations
 */
function displaySkills(skills) {
    try {
        const skillsList = document.getElementById('skillsList');

        if (!skillsList) {
            throw new Error('Skills list element not found');
        }

        if (!skills || skills.length === 0) {
            skillsList.innerHTML = '<div class="empty-skills">📋 No recognized skills found in resume</div>';
            return;
        }

        // Clear existing skills
        skillsList.innerHTML = '';

        // Add skills with staggered animation
        skills.forEach((skill, index) => {
            const skillTag = document.createElement('div');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill.charAt(0).toUpperCase() + skill.slice(1);
            skillTag.style.animationDelay = `${index * 50}ms`;

            skillsList.appendChild(skillTag);
        });
    } catch (error) {
        console.error('Error displaying skills:', error);
        document.getElementById('skillsList').innerHTML = '<div class="empty-skills">⚠️ Error loading skills</div>';
    }
}

/**
 * Display ATS scoring factors with individual scores
 */
function displayFactors(factors) {
    try {
        const factorsList = document.getElementById('factorsList');
        if (!factorsList) return;

        if (!factors || factors.length === 0) {
            factorsList.innerHTML = '<p class="empty-message">No factor data available</p>';
            return;
        }

        const factorIcons = {
            'Keyword Match': '🔍',
            'Skills Alignment': '🛠️',
            'Job Title & Seniority': '👔',
            'Education & Certifications': '🎓',
            'Experience Years': '📅',
            'Resume Formatting': '📄'
        };

        factorsList.innerHTML = '';

        factors.forEach((factor, index) => {
            const factorCard = document.createElement('div');
            factorCard.className = 'factor-card';
            factorCard.style.animationDelay = `${index * 100}ms`;

            // BUG FIX #3: Calculate correct percentage from score/max_score
            const scorePercent = Math.round((factor.score / (factor.max_score || 100)) * 100);
            
            // BUG FIX #4: Calculate letter grade from factor score
            const factorGrade = getLetterGrade(scorePercent);
            const scoreColor = getScoreColor(scorePercent);
            
            // BUG FIX #3: Fix weight display - multiply by 100 to show percentage
            const weightPercent = Math.round(factor.weight * 100);
            
            const icon = factorIcons[factor.name] || '📋';
            
            // Determine feedback label based on score
            let feedbackLabel = 'Needs Improvement';
            if (scorePercent >= 80) feedbackLabel = 'Strong';
            else if (scorePercent >= 60) feedbackLabel = 'Good';
            else if (scorePercent >= 40) feedbackLabel = 'Fair';

            factorCard.innerHTML = `
                <div class="factor-header">
                    <div class="factor-title-group">
                        <span class="factor-icon">${icon}</span>
                        <h4 class="factor-name">${factor.name || 'Unknown'}</h4>
                    </div>
                    <span class="factor-grade" style="background-color: ${scoreColor}; color: white;">${factorGrade}</span>
                </div>
                <div class="factor-score-bar">
                    <div class="factor-score-fill" style="width: ${scorePercent}%; background-color: ${scoreColor};"></div>
                </div>
                <div class="factor-meta">
                    <span class="factor-score">${Math.round(factor.score)}/${factor.max_score || 100} points</span>
                    <span class="factor-weight">${weightPercent}% weight</span>
                </div>
                <p class="factor-feedback-label">${feedbackLabel}</p>
                ${factor.feedback ? `<p class="factor-feedback">${factor.feedback}</p>` : ''}
            `;

            // Add left border with score color
            factorCard.style.borderLeftColor = scoreColor;

            factorsList.appendChild(factorCard);
        });
    } catch (error) {
        console.error('Error displaying factors:', error);
    }
}

/**
 * Display resume strengths
 */
function displayStrengths(strengths) {
    try {
        const strengthsList = document.getElementById('strengthsList');
        if (!strengthsList) return;

        if (!strengths || strengths.length === 0) {
            strengthsList.innerHTML = '<p class="empty-message">No strengths identified</p>';
            return;
        }

        strengthsList.innerHTML = '';

        strengths.forEach((strength, index) => {
            const strengthItem = document.createElement('li');
            strengthItem.className = 'strength-item';
            strengthItem.style.animationDelay = `${index * 100}ms`;
            strengthItem.innerHTML = `
                <span class="strength-checkmark">✓</span>
                <span class="strength-text">${strength}</span>
            `;
            strengthsList.appendChild(strengthItem);
        });
    } catch (error) {
        console.error('Error displaying strengths:', error);
    }
}

/**
 * Display missing keywords that should be added
 */
function displayMissingKeywords(keywords) {
    try {
        const missingList = document.getElementById('missingList');
        if (!missingList) return;

        if (!keywords || keywords.length === 0) {
            missingList.innerHTML = '<p class="empty-message">All key terms from job description found!</p>';
            return;
        }

        missingList.innerHTML = '';

        // Display top 5 missing keywords
        const topMissing = keywords.slice(0, 5);
        topMissing.forEach((keyword, index) => {
            const keywordItem = document.createElement('li');
            keywordItem.className = 'keyword-item';
            keywordItem.style.animationDelay = `${index * 100}ms`;

            // Determine priority based on position in list
            let priority = '🔴 High';
            if (index === 1 || index === 2) priority = '🟡 Medium';
            if (index >= 3) priority = '🟢 Low';

            keywordItem.innerHTML = `
                <span class="keyword-priority">${priority}</span>
                <span class="keyword-text">${keyword}</span>
            `;
            missingList.appendChild(keywordItem);
        });

        // Show count if more than 5
        if (keywords.length > 5) {
            const moreItem = document.createElement('li');
            moreItem.className = 'keyword-item more-item';
            moreItem.textContent = `+${keywords.length - 5} more keywords`;
            missingList.appendChild(moreItem);
        }
    } catch (error) {
        console.error('Error displaying missing keywords:', error);
    }
}

/**
 * Display improvement suggestions
 */
function displaySuggestions(suggestions) {
    try {
        const suggestionsList = document.getElementById('suggestionsList');
        if (!suggestionsList) return;

        if (!suggestions || Object.keys(suggestions).length === 0) {
            suggestionsList.innerHTML = '<p class="empty-message">No suggestions available</p>';
            return;
        }

        suggestionsList.innerHTML = '';
        let suggestionIndex = 0;

        for (const [factor, items] of Object.entries(suggestions)) {
            if (!items || items.length === 0) continue;

            const factorSection = document.createElement('div');
            factorSection.className = 'suggestion-section';
            factorSection.style.animationDelay = `${suggestionIndex * 100}ms`;
            suggestionIndex++;

            const factorTitle = document.createElement('h5');
            factorTitle.className = 'suggestion-factor';
            factorTitle.textContent = factor.replace(/_/g, ' ').toUpperCase();
            factorSection.appendChild(factorTitle);

            const itemsList = document.createElement('ul');
            itemsList.className = 'suggestion-items';

            items.forEach((item, idx) => {
                const li = document.createElement('li');
                li.className = 'suggestion-item';
                li.style.animationDelay = `${(suggestionIndex + idx * 0.5) * 50}ms`;
                li.textContent = item;
                itemsList.appendChild(li);
            });

            factorSection.appendChild(itemsList);
            suggestionsList.appendChild(factorSection);
        }
    } catch (error) {
        console.error('Error displaying suggestions:', error);
    }
}

/**
 * Display warnings about resume quality
 */
function displayWarnings(warnings) {
    try {
        const warningsContainer = document.getElementById('warningsContainer');
        if (!warningsContainer) return;

        if (!warnings || warnings.length === 0) {
            warningsContainer.style.display = 'none';
            return;
        }

        warningsContainer.style.display = 'block';
        warningsContainer.innerHTML = '';

        warnings.forEach((warning, index) => {
            const warningItem = document.createElement('div');
            warningItem.className = 'warning-item';
            warningItem.style.animationDelay = `${index * 100}ms`;
            warningItem.innerHTML = `
                <span class="warning-icon">⚠️</span>
                <span class="warning-text">${warning}</span>
            `;
            warningsContainer.appendChild(warningItem);
        });
    } catch (error) {
        console.error('Error displaying warnings:', error);
    }
}

// ============================================================================
// ERROR HANDLING
// ============================================================================

/**
 * Display error message to user
 */
function showError(message) {
    try {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        // Auto-scroll to error
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
        console.error('Error showing error message:', error);
    }
}

// ============================================================================
// RESET & CLEANUP
// ============================================================================

/**
 * Reset analyzer to initial state and clear all data
 */
function resetAnalyzer() {
    try {
        // Cancel any ongoing analysis
        if (appState.currentAbortController) {
            appState.currentAbortController.abort();
        }

        appState.isAnalyzing = false;

        // Clear file name display
        const fileNameElement = document.getElementById('fileName');
        if (fileNameElement) {
            fileNameElement.textContent = '';
        }

        // Clear file input
        const fileInput = getFileInput();
        if (fileInput) {
            fileInput.value = '';
        }

        // Hide results and errors
        resultsSection.classList.add('hidden');
        errorDiv.classList.add('hidden');

        // Reset upload box HTML and recreate file input
        uploadBox.innerHTML = `
            <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <h2>Upload Your Resume</h2>
            <p>Drag and drop your PDF or click to browse</p>
            <input type="file" id="fileInput" accept=".pdf" hidden>
            <button class="btn-primary" id="chooseFileBtn" title="Select a PDF file to analyze">
                Choose File
            </button>
            <p class="file-info" id="fileName"></p>
        `;

        // Reattach event listeners to new file input
        attachFileInputListener();

        // Attach click handler to new button
        attachChooseFileBtnListener();

        // Reset progress ring
        const circle = document.querySelector('.progress-ring-circle');
        if (circle) {
            circle.classList.remove('filled');
            circle.style.strokeDashoffset = '';
        }

        // Reset score counter
        const scoreValue = document.getElementById('scoreValue');
        if (scoreValue) {
            scoreValue.textContent = '0';
        }

        // Smooth scroll back to upload section
        uploadBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
        console.error('Error resetting analyzer:', error);
        showError('❌ Error resetting form. Please refresh the page.');
    }
}

// ============================================================================
// EVENT LISTENERS & INITIALIZATION
// ============================================================================

/**
 * Delegate file selection to upload box click
 */
function setupUploadBoxClickListener() {
    try {
        uploadBox.addEventListener('click', function(e) {
            // Only trigger if not clicking on button or file input
            if (!e.target.closest('button') && !e.target.closest('input')) {
                const fileInput = getFileInput();
                if (fileInput && !appState.isAnalyzing) {
                    fileInput.click();
                }
            }
        });
    } catch (error) {
        console.error('Error setting up upload box click listener:', error);
    }
}

// Initialize file input listener
attachFileInputListener();
setupUploadBoxClickListener();
attachChooseFileBtnListener();

// Attach click handler to reset button
document.addEventListener('DOMContentLoaded', () => {
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetAnalyzer);
    }

    // Character counter for job description textarea
    const jobDescTextarea = document.getElementById('jobDescription');
    const charCount = document.getElementById('charCount');
    
    if (jobDescTextarea && charCount) {
        const updateCharCount = () => {
            const count = jobDescTextarea.value.length;
            charCount.textContent = `${count} character${count !== 1 ? 's' : ''}`;
            
            // Add active class when there are characters
            if (count > 0) {
                charCount.classList.add('active');
            } else {
                charCount.classList.remove('active');
            }
        };
        
        jobDescTextarea.addEventListener('input', updateCharCount);
        jobDescTextarea.addEventListener('change', updateCharCount);
    }
});

// Add keyboard accessibility
document.addEventListener('keydown', (e) => {
    // Allow Escape key to cancel analysis
    if (e.key === 'Escape' && appState.isAnalyzing) {
        if (appState.currentAbortController) {
            appState.currentAbortController.abort();
        }
        appState.isAnalyzing = false;
    }
});
