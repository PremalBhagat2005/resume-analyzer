# List of technical and professional skills to search for in resumes
import re

skills_list = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "kotlin",
    
    # Web Technologies
    "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle", "cassandra", "redis",
    
    # Data & Analytics
    "machine learning", "data analysis", "excel", "power bi", "tableau", "pandas", 
    "numpy", "scikit-learn", "tensorflow", "pytorch",
    
    # Cloud & DevOps
    "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "git",
    
    # Soft Skills
    "communication", "leadership", "teamwork", "problem solving", "project management"
]

# Function to extract skills found in the given text
def extract_skill(text):
    """
    Search for skills in the provided text (case-insensitive) using word boundaries
    
    Args:
        text (str): The text to search for skills (usually resume content)
    
    Returns:
        list: A list of found skills, with duplicates removed
    """
    # Convert input text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Create an empty list to store found skills
    found = []
    
    # Loop through each skill in our skills list
    for skill in skills_list:
        # Use word boundary regex to match whole words only
        # \b ensures we match word boundaries, not substrings
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            # Add the skill to the found list
            found.append(skill)
    
    # Remove duplicate skills and return
    return list(set(found))


# Function to categorize skills by type
def categorize_skills(skills):
    """
    Group skills into categories (e.g., programming, databases, soft skills)
    
    Args:
        skills (list): List of skills to categorize
    
    Returns:
        dict: Dictionary with skill categories as keys and lists of skills as values
    """
    # Define skill categories with their keywords
    categories = {
        "Programming Languages": ["python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "kotlin"],
        "Web Technologies": ["html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask"],
        "Databases": ["sql", "mysql", "postgresql", "mongodb", "oracle", "cassandra", "redis"],
        "Data & Analytics": ["machine learning", "data analysis", "excel", "power bi", "tableau", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"],
        "Cloud & DevOps": ["aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "git"],
        "Soft Skills": ["communication", "leadership", "teamwork", "problem solving", "project management"]
    }
    
    # Create a result dictionary to store categorized skills
    result = {category: [] for category in categories}
    
    # Loop through each found skill
    for skill in skills:
        # Loop through each category
        for category, category_skills in categories.items():
            # Check if the skill belongs to this category
            if skill.lower() in category_skills:
                # Add skill to the category
                result[category].append(skill)
                # Stop searching once we find the category
                break
    
    # Return only categories that have skills
    return {cat: skill_list for cat, skill_list in result.items() if skill_list}


# Function to score how many skills were found (out of total possible)
def calculate_skill_score(skills):
    """
    Calculate a score representing how many skills were found
    
    Args:
        skills (list): List of found skills
    
    Returns:
        dict: Dictionary with skill count and percentage score
    """
    # Get the number of skills found
    found_count = len(skills)
    
    # Calculate total possible skills in our database
    total_skills = len(skills_list)
    
    # Calculate percentage score
    percentage = (found_count / total_skills) * 100 if total_skills > 0 else 0
    
    # Return the score information as a dictionary
    return {
        "skills_found": found_count,
        "total_skills_available": total_skills,
        "percentage": round(percentage, 2)
    }