"""
Resume Scoring Module
Calculates ATS (Applicant Tracking System) compatibility scores based on skill detection
"""

from skill import skills_list
from typing import Set
import logging

logger = logging.getLogger(__name__)


def calculate_score(found_skills: Set[str]) -> float:
    """
    Calculate the skill match score as a percentage based on detected skills.
    
    The score represents how many of the known skills from the skills database
    are present in the resume. A higher score indicates better alignment with
    typical job requirements.
    
    Scoring Formula:
        score = (number of unique skills found / total unique skills in database) × 100
    
    Args:
        found_skills (Set[str]): Set of unique skills detected in the resume
        
    Returns:
        float: Score as a percentage (0-100), rounded to 2 decimal places
        
    Raises:
        TypeError: If found_skills is not a set or list
        
    Example:
        >>> found = {'python', 'react', 'docker'}
        >>> score = calculate_score(found)
        >>> 0 <= score <= 100
        True
        >>> type(score) == float
        True
    
    Note:
        - Empty resume text (no skills found) will return a score of 0.0
        - A resume with all possible skills would score 100.0
        - Scores are normalized to provide meaningful feedback to users
    """
    try:
        # Validate input type
        if not isinstance(found_skills, (set, list)):
            logger.error(f"Invalid type for found_skills: {type(found_skills)}")
            raise TypeError("found_skills must be a set or list")
        
        # Convert to set if it's a list
        if isinstance(found_skills, list):
            found_skills = set(found_skills)
        
        # Get total number of skills in the database
        total_skills = len(skills_list)
        
        # Handle edge case: empty skills database
        if total_skills == 0:
            logger.warning("Skills list is empty")
            return 0.0
        
        # Calculate the percentage of skills found
        score = (len(found_skills) / total_skills) * 100
        
        # Round to 2 decimal places for precision
        score_rounded = round(score, 2)
        
        logger.info(f"Calculated score: {score_rounded}% ({len(found_skills)}/{total_skills} skills)")
        
        return score_rounded
        
    except Exception as e:
        logger.error(f"Error calculating score: {str(e)}", exc_info=True)
        return 0.0


def get_score_feedback(score: float) -> str:
    """
    Generate human-readable feedback based on the calculated score.
    
    Provides encouraging or actionable feedback to help users improve their resume.
    
    Args:
        score (float): The calculated ATS score (0-100)
        
    Returns:
        str: Human-readable feedback message with emoji indicator
        
    Example:
        >>> feedback = get_score_feedback(85)
        >>> "Excellent" in feedback
        True
    """
    try:
        if score >= 80:
            return "✅ Excellent! Your resume has strong skill alignment."
        elif score >= 60:
            return "👍 Good! Your resume is well-optimized. Consider adding more relevant skills."
        elif score >= 40:
            return "⚠️ Fair score. Adding more relevant skills could improve your ATS ranking."
        else:
            return "❌ Low score. Consider adding more industry-relevant skills to your resume."
    except Exception as e:
        logger.error(f"Error generating score feedback: {str(e)}")
        return "Unable to generate feedback"