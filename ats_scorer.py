"""
ATS scoring engine - calculates match between resume and job description
based on 6 factors: keywords, skills, seniority, education, experience, formatting
"""

import re
import logging
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from collections import Counter

logger = logging.getLogger(__name__)

# Data classes for results

@dataclass
class FactorScore:
    """Represents a single scoring factor result"""
    name: str
    weight: float
    score: float
    max_score: float = 100.0
    feedback: str = ""
    
    def weighted_score(self) -> float:
        """Calculate weighted contribution to total score"""
        return (self.score / self.max_score) * self.weight

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ATSScoreResult:
    """Complete ATS scoring result"""
    total_score: float
    grade: str
    classification: str
    factor_scores: List[FactorScore]
    missing_keywords: List[str]
    strengths: List[str]
    suggestions: Dict[str, str]
    warnings: List[str]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'total_score': round(self.total_score, 2),
            'grade': self.grade,
            'classification': self.classification,
            'factors': [f.to_dict() for f in self.factor_scores],
            'missing_keywords': self.missing_keywords[:5],
            'strengths': self.strengths[:3],
            'suggestions': self.suggestions,
            'warnings': self.warnings
        }


# Skill lists

# Hard Skills Categories
HARD_SKILLS = {
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby",
        "go", "rust", "kotlin", "swift", "matlab", "scala", "r", "perl"
    ],
    "web_frameworks": [
        "react", "angular", "vue", "node.js", "express", "django", "flask",
        "asp.net", "rails", "spring", "laravel", "fastapi", ".net"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "mongodb", "oracle", "cassandra", "redis",
        "elasticsearch", "dynamodb", "firebase", "neo4j", "mariadb"
    ],
    "cloud_platforms": [
        "aws", "azure", "google cloud", "gcp", "heroku", "digitalocean"
    ],
    "devops_tools": [
        "docker", "kubernetes", "jenkins", "gitlab", "github", "git",
        "terraform", "ansible", "ci/cd"
    ],
    "data_ml": [
        "machine learning", "data analysis", "tensorflow", "pytorch", "keras",
        "scikit-learn", "pandas", "numpy", "spark", "hadoop"
    ]
}

# Soft Skills
SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "project management", "critical thinking", "analytical", "creativity",
    "time management", "adaptability", "collaboration", "negotiation"
]

# Seniority Levels
SENIORITY_KEYWORDS = {
    "junior": ["junior", "entry level", "entry-level", "associate"],
    "mid": ["mid-level", "mid level", "intermediate", "senior"],
    "senior": ["senior", "lead", "principal", "architect", "manager"],
    "executive": ["director", "vp", "vice president", "cto", "ceo", "cfo"]
}

# Education Qualifications
EDUCATION_KEYWORDS = {
    "bachelors": ["bachelor", "b.s.", "b.sc.", "undergraduate"],
    "masters": ["master", "m.s.", "m.a.", "m.tech"],
    "phd": ["phd", "ph.d.", "doctorate"],
    "bootcamp": ["bootcamp", "certification course", "intensive"]
}

# Certifications
CERTIFICATIONS = [
    "aws certified", "azure certified", "gcp certified",
    "pmp", "scrum master", "certified kubernetes",
    "cpa", "cfa", "cissp", "ccnp", "ccna"
]

# Synonym Mapping for Action Verbs
VERB_SYNONYMS = {
    "managed": ["led", "oversaw", "directed", "supervised", "coordinated"],
    "built": ["developed", "engineered", "created", "constructed", "implemented"],
    "improved": ["optimized", "enhanced", "streamlined", "accelerated", "boosted"],
    "analyzed": ["evaluated", "assessed", "examined", "reviewed", "inspected"],
    "designed": ["architected", "conceived", "planned", "structured"]
}

# Filler Words to Exclude from Keyword Analysis
FILLER_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "can", "this", "that"
}


# Factor 1: Keyword Match (30%)

def extract_keywords_from_jd(job_description: str, weight_by_position: bool = True) -> Dict[str, Tuple[float, List[str]]]:
    """
    Extract keywords from job description with position weighting.
    """
    try:
        if not job_description or len(job_description) < 50:
            logger.warning("Job description too short for effective keyword extraction")
            return {}
        
        # Normalize text
        text = job_description.lower()
        
        # Split into sections (rough detection)
        sections = {
            "title": text[:200] if len(text) > 200 else text,
            "requirements": text,
            "responsibilities": text
        }
        
        keywords = {}
        
        # Extract multi-word phrases first (bigrams)
        bigram_patterns = [
            r'\b(machine learning|deep learning|data science|project management|team lead|' +
            r'software engineer|full stack|front end|back end|devops engineer|rest api|' +
            r'cloud computing|agile development|quality assurance|web development|' +
            r'mobile app|database design|system design)\b'
        ]
        
        for pattern in bigram_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                normalized = match.lower().strip()
                if normalized not in FILLER_WORDS:
                    weight = 2.0 if normalized in sections.get("title", "") else 1.0
                    keywords[normalized] = (weight, ["phrase"])
        
        # Extract single technical keywords (3+ chars, not filler)
        words = re.findall(r'\b[a-z0-9+#\.]+\b', text)
        word_freq = Counter(words)
        
        for word, freq in word_freq.items():
            if len(word) >= 3 and word not in FILLER_WORDS and word not in keywords:
                # Apply frequency-based weight (but penalize over-repetition)
                freq_weight = min(freq / 5.0, 2.0)  # Cap at 2.0
                keywords[word] = (freq_weight, ["keyword"])
        
        logger.debug(f"Extracted {len(keywords)} keywords from job description")
        return keywords
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}")
        return {}


def calculate_keyword_match(resume_text: str, job_keywords: Dict[str, Tuple[float, List[str]]]) -> FactorScore:
    """
    Calculates keyword matching score (Factor 1: 30% weight).
    """
    try:
        if not job_keywords:
            logger.warning("No job keywords provided for matching")
            return FactorScore(
                name="Keyword Match",
                weight=0.30,
                score=50.0,
                feedback="No job description provided for comparison"
            )
        
        resume_lower = resume_text.lower()
        matched_keywords = {}
        total_weight = sum(w for w, _ in job_keywords.values())
        
        for keyword, (weight, _) in job_keywords.items():
            # Exact match
            if re.search(r'\b' + re.escape(keyword) + r'\b', resume_lower):
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', resume_lower))
                # Penalize if repeated more than 5 times (keyword stuffing)
                mention_weight = min(count / 5.0, 2.0)
                matched_keywords[keyword] = weight * mention_weight
            
            # Partial match for technical terms (e.g., "python" matches "python3")
            elif any(keyword in word for word in resume_lower.split() if len(word) > 3):
                matched_keywords[keyword] = weight * 0.7
        
        # Calculate score
        matched_weight = sum(matched_keywords.values())
        keyword_score = (matched_weight / total_weight * 100) if total_weight > 0 else 0
        keyword_score = min(keyword_score, 100.0)
        
        # Determine feedback
        if keyword_score >= 80:
            feedback = f"Excellent keyword alignment ({len(matched_keywords)}/{len(job_keywords)} keywords matched)"
        elif keyword_score >= 55:
            feedback = f"Good keyword coverage ({len(matched_keywords)}/{len(job_keywords)} keywords found)"
        else:
            feedback = f"Limited keyword match ({len(matched_keywords)}/{len(job_keywords)} keywords found)"
        
        logger.debug(f"Keyword Match Score: {keyword_score:.1f}")
        
        return FactorScore(
            name="Keyword Match",
            weight=0.30,
            score=keyword_score,
            feedback=feedback
        )
        
    except Exception as e:
        logger.error(f"Error calculating keyword match: {str(e)}")
        return FactorScore(
            name="Keyword Match",
            weight=0.30,
            score=0.0,
            feedback="Error in keyword analysis"
        )


# Factor 2: Skills Alignment (25%)

def extract_skills_from_resume(resume_text: str) -> Tuple[List[str], List[str]]:
    """
    Extract hard and soft skills from resume.
    
    Returns:
        Tuple of (hard_skills, soft_skills)
    """
    resume_lower = resume_text.lower()
    hard_skills = []
    soft_skills = []
    
    # Extract hard skills
    for category, skills in HARD_SKILLS.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', resume_lower):
                hard_skills.append(skill)
    
    # Extract soft skills
    for skill in SOFT_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_lower):
            soft_skills.append(skill)
    
    return list(set(hard_skills)), list(set(soft_skills))


def calculate_skills_alignment(resume_text: str, job_keywords: Dict[str, Tuple[float, List[str]]]) -> FactorScore:
    """
    Calculates skills alignment score (Factor 2: 25% weight).
    """
    try:
        hard_skills, soft_skills = extract_skills_from_resume(resume_text)
        
        # If no job description provided, score based on skill presence
        if not job_keywords:
            base_score = min(len(hard_skills) / 5 * 70, 70)  # Cap at 70 for hard skills
            soft_score = min(len(soft_skills) / 3 * 30, 30)  # Cap at 30 for soft skills
            skills_score = base_score + soft_score
            feedback = f"General profile: {len(hard_skills)} hard skills, {len(soft_skills)} soft skills found"
            return FactorScore(
                name="Skills Alignment",
                weight=0.25,
                score=min(skills_score, 100.0),
                feedback=feedback
            )
        
        # Identify required skills from job description
        required_hard_skills = set()
        for keyword in job_keywords.keys():
            for category, skills in HARD_SKILLS.items():
                if keyword in skills:
                    required_hard_skills.add(keyword)
        
        # Calculate alignment
        hard_skill_match = len(set(hard_skills) & required_hard_skills) / len(required_hard_skills) * 70 if required_hard_skills else 0
        soft_skill_presence = min(len(soft_skills) / 3 * 30, 30)  # Cap at 30 points
        
        skills_score = hard_skill_match + soft_skill_presence
        
        feedback = f"Hard skills: {len(hard_skills)} found | Soft skills: {len(soft_skills)} found"
        
        logger.debug(f"Skills Alignment Score: {skills_score:.1f}")
        
        return FactorScore(
            name="Skills Alignment",
            weight=0.25,
            score=min(skills_score, 100.0),
            feedback=feedback
        )
        
    except Exception as e:
        logger.error(f"Error calculating skills alignment: {str(e)}")
        return FactorScore(
            name="Skills Alignment",
            weight=0.25,
            score=50.0,
            feedback="Error in skills analysis"
        )



def extract_job_titles_and_seniority(resume_text: str) -> Tuple[List[str], str]:
    """
    Extract job titles and detect seniority level from resume.
    
    Returns:
        Tuple of (job_titles, detected_seniority_level)
    """
    resume_lower = resume_text.lower()
    titles = re.findall(r'(?:title|position|role)[:\s]+([a-z\s]+?)(?:\n|,|$)', resume_lower)
    
    # Detect seniority
    for level, keywords in SENIORITY_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', resume_lower):
                return titles, level
    
    return titles, "mid"  # Default to mid-level


def calculate_seniority_match(resume_text: str, job_keywords: Dict[str, Tuple[float, List[str]]]) -> FactorScore:
    """
    Calculates seniority and job title match (Factor 3: 15% weight).
    """
    try:
        job_titles, detected_seniority = extract_job_titles_and_seniority(resume_text)
        
        # If no job description provided, score based on detected seniority
        if not job_keywords:
            seniority_scores = {"junior": 50, "mid": 75, "senior": 95, "executive": 100}
            seniority_score = seniority_scores.get(detected_seniority, 60)
            feedback = f"Detected seniority: {detected_seniority.title()} | Job titles: {len(job_titles)}"
            logger.debug(f"Seniority Match Score: {seniority_score:.1f}")
            return FactorScore(
                name="Job Title & Seniority",
                weight=0.15,
                score=seniority_score,
                feedback=feedback
            )
        
        # Detect required seniority from job keywords
        required_seniority = "mid"
        for level, keywords in SENIORITY_KEYWORDS.items():
            for keyword in keywords:
                if any(keyword in str(k) for k in job_keywords.keys()):
                    required_seniority = level
                    break
        
        # Score based on match
        seniority_scores = {"junior": 1, "mid": 2, "senior": 3, "executive": 4}
        detected_score = seniority_scores.get(detected_seniority, 2)
        required_score = seniority_scores.get(required_seniority, 2)
        
        # Perfect match = 100, under-qualified = 40, over-qualified = 80
        if detected_score == required_score:
            seniority_score = 100.0
        elif detected_score < required_score:
            seniority_score = max(40.0, (detected_score / required_score) * 100)
        else:
            seniority_score = 80.0
        
        feedback = f"Detected: {detected_seniority.title()} | Required: {required_seniority.title()}"
        
        logger.debug(f"Seniority Match Score: {seniority_score:.1f}")
        
        return FactorScore(
            name="Job Title & Seniority",
            weight=0.15,
            score=seniority_score,
            feedback=feedback
        )
        
    except Exception as e:
        logger.error(f"Error calculating seniority match: {str(e)}")
        return FactorScore(
            name="Job Title & Seniority",
            weight=0.15,
            score=60.0,
            feedback="Unable to determine seniority level"
        )


# Factor 4: Education & Certifications (10%)

def calculate_education_score(resume_text: str) -> FactorScore:
    """
    Calculates education match score (Factor 4: 10% weight).
    """
    try:
        resume_lower = resume_text.lower()
        
        education_score = 0.0
        has_degree = False
        
        # Check for degrees
        for degree_type, keywords in EDUCATION_KEYWORDS.items():
            for keyword in keywords:
                if re.search(r'\b' + keyword + r'\b', resume_lower):
                    has_degree = True
                    if degree_type == "phd":
                        education_score += 40.0
                    elif degree_type == "masters":
                        education_score += 30.0
                    elif degree_type == "bachelors":
                        education_score += 25.0
                    else:
                        education_score += 15.0
                    break
        
        # Check for certifications
        certifications_found = 0
        for cert in CERTIFICATIONS:
            if re.search(r'\b' + re.escape(cert) + r'\b', resume_lower):
                certifications_found += 1
                education_score += 10.0
        
        education_score = min(education_score, 100.0)
        
        feedback = f"Education: {'Yes' if has_degree else 'Not detected'} | Certifications: {certifications_found}"
        
        logger.debug(f"Education Score: {education_score:.1f}")
        
        return FactorScore(
            name="Education & Certifications",
            weight=0.10,
            score=education_score,
            feedback=feedback
        )
        
    except Exception as e:
        logger.error(f"Error calculating education score: {str(e)}")
        return FactorScore(
            name="Education & Certifications",
            weight=0.10,
            score=50.0,
            feedback="Error in education analysis"
        )


# Factor 5: Experience Years (10%)

def extract_years_of_experience(resume_text: str) -> float:
    """
    Extract estimated total years of experience from resume.
    
    Returns:
        Estimated number of years
    """
    # Look for explicit year ranges
    year_ranges = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', resume_text, re.IGNORECASE)
    
    total_years = 0.0
    current_year = 2026
    
    for start, end in year_ranges:
        start_year = int(start)
        if end.lower() in ['present', 'current']:
            end_year = current_year
        else:
            end_year = int(end)
        
        total_years += (end_year - start_year)
    
    return total_years


def calculate_experience_score(resume_text: str, job_keywords: Dict[str, Tuple[float, List[str]]]) -> FactorScore:
    """
    Calculates experience years match score (Factor 5: 10% weight).
    """
    try:
        detected_years = extract_years_of_experience(resume_text)
        
        # If no job description provided, score based on years of experience
        if not job_keywords:
            if detected_years == 0:
                years_score = 40.0  # Entry level
            elif detected_years < 2:
                years_score = 55.0  # Junior
            elif detected_years < 5:
                years_score = 75.0  # Mid-level
            elif detected_years < 10:
                years_score = 90.0  # Senior
            else:
                years_score = 100.0  # Very experienced
            feedback = f"Total detected experience: {detected_years:.1f} years"
            logger.debug(f"Experience Score: {years_score:.1f}")
            return FactorScore(
                name="Experience Years",
                weight=0.10,
                score=years_score,
                feedback=feedback
            )
        
        # Try to extract required years from job description
        required_years = 0
        for keyword in job_keywords.keys():
            match = re.search(r'(\d+)\+?\s*years?', keyword.lower())
            if match:
                required_years = max(required_years, int(match.group(1)))
        
        if required_years == 0:
            required_years = 5  # Default assumption
        
        # Calculate score
        if detected_years >= required_years:
            years_score = 100.0
        elif detected_years > 0:
            years_score = (detected_years / required_years) * 100
        else:
            years_score = 0.0  # No experience detected
        
        years_score = min(years_score, 100.0)
        
        feedback = f"Detected: {detected_years:.1f} years | Required: {required_years}+ years"
        
        logger.debug(f"Experience Score: {years_score:.1f}")
        
        return FactorScore(
            name="Experience Years",
            weight=0.10,
            score=years_score,
            feedback=feedback
        )
        
    except Exception as e:
        logger.error(f"Error calculating experience score: {str(e)}")
        return FactorScore(
            name="Experience Years",
            weight=0.10,
            score=50.0,
            feedback="Unable to determine experience level"
        )


# Factor 6: Resume Formatting & Structure (10%)

def calculate_formatting_score(resume_text: str) -> FactorScore:
    """
    Calculates resume formatting and structure score (Factor 6: 10% weight).
    """
    try:
        formatting_score = 50.0  # Base score
        issues = []
        strengths = []
        
        # Check for standard sections
        sections_to_check = {
            r'\b(professional summary|objective|summary)\b': "Summary/Objective",
            r'\b(experience|employment history|work experience)\b': "Experience",
            r'\b(education|qualifications)\b': "Education",
            r'\b(skills|technical skills)\b': "Skills",
            r'\b(contact|phone|email)\b': "Contact Info"
        }
        
        found_sections = 0
        for pattern, section_name in sections_to_check.items():
            if re.search(pattern, resume_text, re.IGNORECASE):
                found_sections += 1
                strengths.append(f"Has {section_name} section")
        
        # Score based on sections (each section +15 points)
        formatting_score = (found_sections / 5) * 70 + 30
        
        # Check for ATS-unfriendly elements
        if '|' in resume_text or '\t' in resume_text:
            issues.append("Contains tables or columns (ATS-unfriendly)")
            formatting_score -= 15
        
        if re.search(r'[®™©]', resume_text):
            issues.append("Contains special symbols that may not parse")
            formatting_score -= 5
        
        # Check resume length
        word_count = len(resume_text.split())
        if word_count < 200:
            issues.append("Resume too short (under 200 words)")
            formatting_score -= 20
        elif word_count > 2000:
            issues.append("Resume too long (over 2000 words)")
            formatting_score -= 10
        else:
            strengths.append(f"Appropriate length ({word_count} words)")
        
        formatting_score = max(0.0, min(formatting_score, 100.0))
        
        feedback = f"Sections: {found_sections}/5 | Issues: {len(issues)}"
        
        logger.debug(f"Formatting Score: {formatting_score:.1f}")
        
        return FactorScore(
            name="Resume Formatting",
            weight=0.10,
            score=formatting_score,
            feedback=feedback
        )
        
    except Exception as e:
        logger.error(f"Error calculating formatting score: {str(e)}")
        return FactorScore(
            name="Resume Formatting",
            weight=0.10,
            score=50.0,
            feedback="Error in formatting analysis"
        )


# Main scoring functions

def calculate_ats_score(
    resume_text: str,
    job_description: Optional[str] = None,
    debug: bool = False
) -> ATSScoreResult:
    """
    Calculate comprehensive ATS score for a resume.
    
    This is the main entry point that combines all 6 factors:
    1. Keyword Match (30%)
    2. Skills Alignment (25%)
    3. Job Title & Seniority (15%)
    4. Education & Certifications (10%)
    5. Experience Years (10%)
    6. Resume Formatting (10%)
    
    Args:
        resume_text: Extracted resume text
        job_description: Optional job description for comparison
        debug: Enable detailed logging of intermediate scores
        
    Returns:
        ATSScoreResult with complete scoring breakdown
    """
    try:
        warnings = []
        
        # Validate inputs
        if not resume_text or len(resume_text) < 100:
            warnings.append("⚠️ Resume is very short (under 100 words). Scoring may not be reliable.")
        
        if not job_description:
            warnings.append("⚠️ No job description provided. Using general quality scoring instead.")
            job_keywords = {}
        else:
            if len(job_description) < 50:
                warnings.append("⚠️ Job description is very short.")
            job_keywords = extract_keywords_from_jd(job_description)
        
        # Calculate individual factor scores
        if debug:
            logger.info("=== ATS SCORING DEBUG START ===")
        
        factor1 = calculate_keyword_match(resume_text, job_keywords)
        if debug: logger.info(f"Factor 1 (Keyword Match): {factor1.score:.1f}")
        
        factor2 = calculate_skills_alignment(resume_text, job_keywords)
        if debug: logger.info(f"Factor 2 (Skills Alignment): {factor2.score:.1f}")
        
        factor3 = calculate_seniority_match(resume_text, job_keywords)
        if debug: logger.info(f"Factor 3 (Seniority): {factor3.score:.1f}")
        
        factor4 = calculate_education_score(resume_text)
        if debug: logger.info(f"Factor 4 (Education): {factor4.score:.1f}")
        
        factor5 = calculate_experience_score(resume_text, job_keywords)
        if debug: logger.info(f"Factor 5 (Experience): {factor5.score:.1f}")
        
        factor6 = calculate_formatting_score(resume_text)
        if debug: logger.info(f"Factor 6 (Formatting): {factor6.score:.1f}")
        
        # Calculate total weighted score
        factor_scores = [factor1, factor2, factor3, factor4, factor5, factor6]
        total_score = sum(f.weighted_score() for f in factor_scores)
        total_score = min(total_score, 100.0)
        
        if debug: logger.info(f"Total ATS Score: {total_score:.1f}")
        
        # Determine grade and classification
        grade, classification = calculate_grade_and_classification(total_score)
        
        # Extract missing keywords and strengths
        missing_keywords = extract_missing_keywords(resume_text, job_keywords)
        strengths = extract_strengths(resume_text, job_keywords, hard_skills=True)
        
        # Generate suggestions for weak factors
        suggestions = generate_suggestions(factor_scores)
        
        if debug:
            logger.info(f"Grade: {grade} | Classification: {classification}")
            logger.info("=== ATS SCORING DEBUG END ===")
        
        return ATSScoreResult(
            total_score=total_score,
            grade=grade,
            classification=classification,
            factor_scores=factor_scores,
            missing_keywords=missing_keywords,
            strengths=strengths,
            suggestions=suggestions,
            warnings=warnings
        )
        
    except Exception as e:
        logger.error(f"Error in ATS scoring: {str(e)}", exc_info=True)
        return ATSScoreResult(
            total_score=0.0,
            grade="F",
            classification="Error in analysis",
            factor_scores=[],
            missing_keywords=[],
            strengths=[],
            suggestions={},
            warnings=[f"❌ Error calculating ATS score: {str(e)}"]
        )



def calculate_grade_and_classification(score: float) -> Tuple[str, str]:
    """Convert score to letter grade and classification"""
    if score >= 90:
        return "A", "Excellent Match — ATS will likely pass this"
    elif score >= 80:
        return "B", "Very Good — Strong candidacy with minor gaps"
    elif score >= 70:
        return "C", "Good Match — Minor improvements needed"
    elif score >= 60:
        return "D", "Fair Match — Moderate gaps detected"
    elif score >= 50:
        return "E", "Average — Significant improvements needed"
    else:
        return "F", "Poor Match — Major revision required"


def extract_missing_keywords(resume_text: str, job_keywords: Dict[str, Tuple[float, List[str]]]) -> List[str]:
    """Extract top missing keywords sorted by weight"""
    resume_lower = resume_text.lower()
    missing = []
    
    for keyword, (weight, _) in sorted(job_keywords.items(), key=lambda x: x[1][0], reverse=True):
        if not re.search(r'\b' + re.escape(keyword) + r'\b', resume_lower):
            missing.append(keyword)
    
    return missing[:10]


def extract_strengths(resume_text: str, job_keywords: Dict[str, Tuple[float, List[str]]], hard_skills: bool = True) -> List[str]:
    """Extract top strengths (matched keywords and skills)"""
    resume_lower = resume_text.lower()
    strengths = []
    
    # Check for matched keywords
    for keyword in job_keywords.keys():
        if re.search(r'\b' + re.escape(keyword) + r'\b', resume_lower):
            strengths.append(f"✓ {keyword.title()}")
    
    # Check for hard skills
    if hard_skills:
        hard_skills_found, _ = extract_skills_from_resume(resume_text)
        for skill in hard_skills_found[:3]:
            strengths.append(f"✓ {skill.title()} proficiency")
    
    return strengths[:10]


def generate_suggestions(factor_scores: List[FactorScore]) -> Dict[str, str]:
    """Generate actionable suggestions for weak factors"""
    suggestions = {}
    
    for factor in sorted(factor_scores, key=lambda x: x.score):
        if factor.score < 70:
            if "Keyword" in factor.name:
                suggestions[factor.name] = "Add more job-specific keywords and technical terms from the job description"
            elif "Skills" in factor.name:
                suggestions[factor.name] = "Highlight relevant technical skills more prominently in your experience section"
            elif "Seniority" in factor.name:
                suggestions[factor.name] = "Adjust your role descriptions to better match the seniority level required"
            elif "Education" in factor.name:
                suggestions[factor.name] = "Add relevant certifications or educational achievements that match job requirements"
            elif "Experience" in factor.name:
                suggestions[factor.name] = "Quantify and highlight relevant years of experience in your current role"
            elif "Formatting" in factor.name:
                suggestions[factor.name] = "Ensure resume has clear sections (Summary, Experience, Education, Skills)"
    
    return suggestions


if __name__ == "__main__":
    # Example usage for testing
    logging.basicConfig(level=logging.DEBUG)
    
    sample_resume = """
    John Doe
    Senior Software Engineer
    john.doe@email.com | (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 7+ years of experience in full-stack development using Python,
    Django, React, and AWS. Strong background in building scalable web applications and leading
    development teams.
    
    EXPERIENCE
    Senior Staff Engineer | TechCorp | 2020-Present
    - Led development of microservices architecture using Docker and Kubernetes
    - Improved application performance by 40% through optimization
    - Managed team of 5 developers
    
    Software Engineer | StartupXyz | 2018-2020
    - Built REST APIs using Django and Python
    - Developed React components for frontend
    - Managed PostgreSQL databases
    
    EDUCATION
    Bachelor of Science in Computer Science | State University | 2018
    
    SKILLS
    Languages: Python, JavaScript, TypeScript, Java
    Frameworks: Django, React, Express.js
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS (EC2, S3, Lambda), Google Cloud
    DevOps: Docker, Kubernetes, Jenkins, Git
    """
    
    sample_jd = """
    Senior Full-Stack Developer
    
    We are looking for a Senior Full-Stack Developer with 5+ years of experience.
    
    Required Skills:
    - Python and JavaScript expertise
    - React or Angular
    - PostgreSQL and MongoDB
    - AWS and Docker
    - Strong problem solving and communication
    
    Responsibilities:
    - Develop and maintain scalable web applications
    - Design microservices architecture
    - Lead code reviews and mentor junior developers
    - Optimize application performance
    
    Nice to have:
    - Kubernetes experience
    - CI/CD experience
    - AWS certifications
    """
    
    result = calculate_ats_score(sample_resume, sample_jd, debug=True)
    print(result.to_dict())
