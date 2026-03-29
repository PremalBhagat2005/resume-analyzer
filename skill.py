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
    """Finds all technical skills mentioned in the text."""
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
    """Groups skills by category (languages, frameworks, databases, etc)."""
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
    """Returns recommended skills to add that aren't yet in the resume."""
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