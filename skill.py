"""
Skill Extraction Module
Identifies and categorizes technical and professional skills found in resume text
"""

import re
import logging
from typing import List, Dict, Set

logger = logging.getLogger(__name__)

# Comprehensive list of technical and professional skills to search for in resumes
skills_list = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "kotlin",
    "matlab", "scala", "r", "swift", "objective-c", "typescript", "perl",
    
    # Web Technologies & Frameworks
    "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask",
    "asp.net", "rails", "spring", "laravel", "fastapi", "gtk", "qt",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle", "cassandra", "redis",
    "elasticsearch", "dynamodb", "firebase", "neo4j", "mariadb",
    
    # Data Science & ML
    "machine learning", "data analysis", "excel", "power bi", "tableau", "pandas", 
    "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "spark", "hadoop",
    "jira", "analytics", "statistics", "data mining",
    
    # Cloud & DevOps
    "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "git",
    "gitlab", "github", "ansible", "terraform", "ci/cd", "devops",
    
    # Tools & Technologies
    "linux", "unix", "windows", "mac", "jira", "confluence", "slack",
    "excel", "word", "powerpoint", "salesforce", "sap",
    
    # Soft Skills
    "communication", "leadership", "teamwork", "problem solving", "project management",
    "agile", "scrum", "kanban", "waterfall", "critical thinking", "analytical"
]


def extract_skill(text: str) -> List[str]:
    """
    Search for technical and professional skills in the provided text.
    
    Uses word boundary regex matching for accurate skill identification.
    Matching is case-insensitive and returns only unique skills found.
    
    Args:
        text (str): The text to search for skills (usually resume content)
        
    Returns:
        List[str]: A list of detected skills with duplicates removed,
                   sorted alphabetically for consistent output
                   
    Example:
        >>> text = "I have 5 years of Python and React experience"
        >>> skills = extract_skill(text)
        >>> 'python' in skills
        True
        >>> 'react' in skills
        True
    """
    try:
        # Convert input text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Use set to automatically remove duplicates
        found_skills: Set[str] = set()
        
        # Search for each skill in the skills list
        for skill in skills_list:
            # Use word boundary regex to match whole words only
            # \b ensures we match complete words, not parts of other words
            # re.escape() handles special regex characters in skill names (e.g., "c++")
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            
            # If skill is found, add to set
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Convert to sorted list for consistent output
        result = sorted(list(found_skills))
        logger.debug(f"Extracted {len(result)} unique skills from text")
        
        return result
        
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}", exc_info=True)
        return []


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """
    Organize skills into semantic categories for better presentation.
    
    This helps recruiters and job seekers understand which skill categories
    are represented in the resume and identify gaps.
    
    Args:
        skills (List[str]): List of skills to categorize
        
    Returns:
        Dict[str, List[str]]: Dictionary with category names as keys
                              and lists of skills as values. Empty categories
                              are excluded from the result.
                              
    Example:
        >>> skills = ['python', 'java', 'docker', 'leadership']
        >>> categorized = categorize_skills(skills)
        >>> categorized['Programming Languages']
        ['java', 'python']
    """
    try:
        # Define skill categories with their keywords for classification
        categories: Dict[str, List[str]] = {
            "Programming Languages": [
                "python", "java", "javascript", "c++", "c#", "php", "ruby", 
                "go", "rust", "kotlin", "matlab", "scala", "r", "swift", 
                "objective-c", "typescript", "perl"
            ],
            "Web Technologies": [
                "html", "css", "react", "angular", "vue", "node.js", "express", 
                "django", "flask", "asp.net", "rails", "spring", "laravel", 
                "fastapi", "gtk", "qt"
            ],
            "Databases": [
                "sql", "mysql", "postgresql", "mongodb", "oracle", "cassandra", 
                "redis", "elasticsearch", "dynamodb", "firebase", "neo4j", "mariadb"
            ],
            "Data Science & ML": [
                "machine learning", "data analysis", "excel", "power bi", "tableau", 
                "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", 
                "spark", "hadoop", "analytics", "statistics", "data mining"
            ],
            "Cloud & DevOps": [
                "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", 
                "git", "gitlab", "github", "ansible", "terraform", "ci/cd", "devops"
            ],
            "Tools & Platforms": [
                "linux", "unix", "windows", "mac", "jira", "confluence", "slack",
                "word", "powerpoint", "salesforce", "sap"
            ],
            "Soft Skills": [
                "communication", "leadership", "teamwork", "problem solving", 
                "project management", "agile", "scrum", "kanban", "waterfall", 
                "critical thinking", "analytical"
            ]
        }
        
        # Populate categories with found skills
        categorized: Dict[str, List[str]] = {}
        
        for category, category_skills in categories.items():
            # Find intersection of found skills and category skills
            found_in_category = [s for s in skills if s.lower() in category_skills]
            
            # Only include categories that have at least one skill
            if found_in_category:
                categorized[category] = sorted(found_in_category)
        
        logger.debug(f"Categorized {len(skills)} skills into {len(categorized)} categories")
        return categorized
        
    except Exception as e:
        logger.error(f"Error categorizing skills: {str(e)}", exc_info=True)
        return {}


def get_skill_recommendations(found_skills: List[str], category: str = "") -> List[str]:
    """
    Suggest missing skills based on found skills and selected category.
    
    Helps users identify complementary skills they should add to improve
    their resume's relevance and competitiveness.
    
    Args:
        found_skills (List[str]): Skills already found in resume
        category (str, optional): Category to focus recommendations on
        
    Returns:
        List[str]: List of recommended skills not yet present in resume
        
    Example:
        >>> found = ['python', 'pandas']
        >>> recommendations = get_skill_recommendations(found, 'Data Science & ML')
        >>> 'tensorflow' in recommendations
        True
    """
    found_set = set(s.lower() for s in found_skills)
    
    if category:
        # Get recommendations from specific category
        category_skills = {
            "Programming Languages": ["python", "java", "javascript", "typescript"],
            "Data Science & ML": ["tensorflow", "pytorch", "spark", "hadoop"],
            "Cloud & DevOps": ["docker", "kubernetes", "jenkins", "terraform"],
        }
        available = set(category_skills.get(category, []))
    else:
        # Get recommendations from all skills
        available = set(skills_list)
    
    # Return skills that are available but not yet found
    recommendations = sorted(list(available - found_set))
    logger.debug(f"Generated {len(recommendations)} skill recommendations")
    
    return recommendations
    
    # Calculate percentage score
    percentage = (found_count / total_skills) * 100 if total_skills > 0 else 0
    
    # Return the score information as a dictionary
    return {
        "skills_found": found_count,
        "total_skills_available": total_skills,
        "percentage": round(percentage, 2)
    }