skills_list = [
    "python", "java", "sql", "machine learning",
    "data analysis", "excel", "power bi", "tableau"
]

def extract_skill(text):
    found = []
    for skill in skills_list:
        if skill in text:
            found.append(skill)
    return found