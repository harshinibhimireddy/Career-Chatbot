"""
Scoring module for subject marks and interest levels based on a predefined rule matrix.
Strictly deterministic without any AI/ML dependencies.
"""

# Scoring Matrix mapping (marks_range, interest_level) -> exact score
SCORING_MATRIX = {
    ("above_75", "very_interested"): 10,
    ("above_75", "interested"): 9,
    ("above_75", "neutral"): 5,
    ("above_75", "not_interested"): 2,

    ("50_75", "very_interested"): 9,
    ("50_75", "interested"): 8,
    ("50_75", "neutral"): 4,
    ("50_75", "not_interested"): 2,

    ("below_50", "very_interested"): 6,
    ("below_50", "interested"): 5,
    ("below_50", "neutral"): 2,
    ("below_50", "not_interested"): 0,
}

# Display mappings for friendly labels
MARKS_DISPLAY = {
    "above_75": "Above 75%",
    "50_75": "50% to 75%",
    "below_50": "Below 50%"
}

INTEREST_DISPLAY = {
    "very_interested": "Very Interested",
    "interested": "Interested",
    "neutral": "Neutral",
    "not_interested": "Not Interested"
}


def calculate_subject_score(marks_range: str, interest_level: str) -> int:
    """
    Calculate score for a subject given academic marks range and interest level.
    
    Parameters:
    - marks_range: 'above_75', '50_75', 'below_50'
    - interest_level: 'very_interested', 'interested', 'neutral', 'not_interested'
    
    Returns:
    - Integer score from 0 to 10 based on matrix.
    """
    key = (marks_range, interest_level)
    return SCORING_MATRIX.get(key, 0)


def compute_all_subject_scores(answers: dict) -> dict:
    """
    Computes scores for all 6 subjects from collected user answers.
    Subjects: math, physics, chemistry, biology, social, language.
    """
    subjects = ["math", "physics", "chemistry", "biology", "social", "language"]
    scores = {}
    for subj in subjects:
        m_key = f"{subj}_marks"
        i_key = f"{subj}_interest"
        m_val = answers.get(m_key, "below_50")
        i_val = answers.get(i_key, "not_interested")
        scores[f"{subj}_score"] = calculate_subject_score(m_val, i_val)
    return scores
