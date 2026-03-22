def calculate_score(found_skills):
    total_skills = 8
    score = (len(found_skills) / total_skills) * 100
    return round(score, 2)