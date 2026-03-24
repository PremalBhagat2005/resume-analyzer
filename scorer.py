from skill import skills_list
from typing import Set

def calculate_score(found_skills: Set[str]) -> float:
    """
    Calculate the skill match score as a percentage.
    
    Args:
        found_skills: Set of skills found in the resume
        
    Returns:
        float: Score as a percentage (0-100), rounded to 2 decimal places
    """
    total_skills = len(skills_list)
    if total_skills == 0:
        return 0.0
    
    score = (len(found_skills) / total_skills) * 100
    return round(score, 2)