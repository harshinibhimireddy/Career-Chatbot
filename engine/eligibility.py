"""
Eligibility engine to evaluate pathway prerequisites against student's academic background.
Strictly separates UI and conversational flow from rule checking logic.
"""

from data.eligibility_rules import ELIGIBILITY_CONSTRAINTS


def check_pathway_eligibility(pathway_id: str, stream: str, answers: dict = None) -> dict:
    """
    Check if a candidate pathway is eligible for a student given their Class 12 stream.
    
    Returns:
    {
        "eligible": True/False,
        "reason": "Explanation string...",
        "is_prerequisite_gap": True/False,
        "suggested_alternatives": list[str]
    }
    """
    rule = ELIGIBILITY_CONSTRAINTS.get(pathway_id)
    if not rule:
        return {
            "eligible": True,
            "reason": "No strict prerequisite constraints found.",
            "is_prerequisite_gap": False,
            "suggested_alternatives": []
        }

    # If stream is in disqualified streams
    if stream in rule.get("disqualified_streams", []):
        # Special check for BiPC students interested in tech
        if stream == "BiPC" and pathway_id in ["btech_cse", "btech_aiml", "btech_ece", "btech_eee", "btech_mech", "btech_civil"]:
            return {
                "eligible": False,
                "reason": (
                    f"Your academic stream ({stream}) does not include Class 12 Mathematics, which is a mandatory "
                    f"prerequisite for standard B.Tech engineering programs. While your interest in technology is high, "
                    f"you cannot directly enroll in standard B.Tech Engineering in this rule-based system. "
                    f"However, life-science technology pathways such as Biomedical Science, Bioinformatics, and "
                    f"Health Informatics are fully eligible for you."
                ),
                "is_prerequisite_gap": True,
                "suggested_alternatives": rule.get("suggested_alternatives", [])
            }
        
        return {
            "eligible": False,
            "reason": rule.get("explanation", "Prerequisite subjects not satisfied for this stream."),
            "is_prerequisite_gap": True,
            "suggested_alternatives": rule.get("suggested_alternatives", [])
        }

    return {
        "eligible": True,
        "reason": "Meets academic stream prerequisites.",
        "is_prerequisite_gap": False,
        "suggested_alternatives": []
    }


def filter_eligible_pathways(candidate_pathways: list, stream: str) -> tuple[list, list]:
    """
    Filters candidate pathways into eligible pathways and ineligible pathways with reasons.
    """
    eligible = []
    ineligible = []

    for pathway in candidate_pathways:
        res = check_pathway_eligibility(pathway["id"], stream)
        if res["eligible"]:
            pathway_copy = pathway.copy()
            pathway_copy["eligibility_status"] = "Eligible"
            eligible.append(pathway_copy)
        else:
            pathway_copy = pathway.copy()
            pathway_copy["eligibility_status"] = "Ineligible"
            pathway_copy["ineligible_reason"] = res["reason"]
            pathway_copy["is_prerequisite_gap"] = res["is_prerequisite_gap"]
            pathway_copy["suggested_alternatives"] = res.get("suggested_alternatives", [])
            ineligible.append(pathway_copy)

    return eligible, ineligible
