"""
Unit and Integration Tests for Career Recommendation Chatbot Engine.
Verifies scoring matrices, decision-tree routing, eligibility rules, and recommendations.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from engine.scoring import calculate_subject_score, compute_all_subject_scores, SCORING_MATRIX
from data.rules import evaluate_class_10_branch, score_class_10_streams
from engine.eligibility import check_pathway_eligibility
from engine.recommendation import generate_class_12_recommendations


def test_scoring_matrix():
    print("Testing scoring matrix...")
    # Above 75%
    assert calculate_subject_score("above_75", "very_interested") == 10
    assert calculate_subject_score("above_75", "interested") == 9
    assert calculate_subject_score("above_75", "neutral") == 5
    assert calculate_subject_score("above_75", "not_interested") == 2

    # 50% to 75%
    assert calculate_subject_score("50_75", "very_interested") == 9
    assert calculate_subject_score("50_75", "interested") == 8
    assert calculate_subject_score("50_75", "neutral") == 4
    assert calculate_subject_score("50_75", "not_interested") == 2

    # Below 50%
    assert calculate_subject_score("below_50", "very_interested") == 6
    assert calculate_subject_score("below_50", "interested") == 5
    assert calculate_subject_score("below_50", "neutral") == 2
    assert calculate_subject_score("below_50", "not_interested") == 0
    print("✓ Scoring matrix passed!")


def test_class_10_decision_tree():
    print("Testing Class 10 decision tree branches...")
    
    # 1. Strong MPC profile
    mpc_answers = {
        "math_marks": "above_75", "math_interest": "very_interested",       # 10
        "physics_marks": "above_75", "physics_interest": "very_interested", # 10
        "chemistry_marks": "50_75", "chemistry_interest": "interested",     # 8
        "biology_marks": "below_50", "biology_interest": "not_interested",  # 0
        "social_marks": "below_50", "social_interest": "not_interested",    # 0
        "language_marks": "below_50", "language_interest": "neutral",       # 2
        "c10_adaptive_primary": "Programming and software",
        "c10_adaptive_followup": "Software & High-Tech Industry"
    }
    branch = evaluate_class_10_branch(mpc_answers)
    assert branch == "mpc_tech", f"Expected mpc_tech, got {branch}"
    recs = score_class_10_streams(mpc_answers)
    assert recs[0]["stream_id"] == "MPC", f"Expected top stream MPC, got {recs[0]['stream_id']}"
    assert recs[0]["match_score"] > 85

    # 2. Strong BiPC profile
    bipc_answers = {
        "math_marks": "below_50", "math_interest": "not_interested",        # 0
        "physics_marks": "50_75", "physics_interest": "interested",         # 8
        "chemistry_marks": "above_75", "chemistry_interest": "interested",  # 9
        "biology_marks": "above_75", "biology_interest": "very_interested", # 10
        "social_marks": "below_50", "social_interest": "neutral",          # 2
        "language_marks": "below_50", "language_interest": "neutral",       # 2
        "c10_adaptive_primary": "Understanding the human body",
        "c10_adaptive_followup": "Hospitals & Direct Patient Care"
    }
    branch = evaluate_class_10_branch(bipc_answers)
    assert branch == "bipc_health", f"Expected bipc_health, got {branch}"
    recs = score_class_10_streams(bipc_answers)
    assert recs[0]["stream_id"] == "BiPC", f"Expected top stream BiPC, got {recs[0]['stream_id']}"

    # 3. Strong PCMB Dual profile (all science & math >= 8)
    pcmb_answers = {
        "math_marks": "above_75", "math_interest": "very_interested",       # 10
        "physics_marks": "above_75", "physics_interest": "very_interested", # 10
        "chemistry_marks": "above_75", "chemistry_interest": "very_interested", # 10
        "biology_marks": "above_75", "biology_interest": "very_interested", # 10
        "social_marks": "below_50", "social_interest": "not_interested",    # 0
        "language_marks": "below_50", "language_interest": "neutral",       # 2
        "c10_adaptive_primary": "Combining biology and technology",
        "c10_adaptive_followup": "Yes, I love the intersection of Bio and Tech"
    }
    branch = evaluate_class_10_branch(pcmb_answers)
    assert branch == "pcmb_dual", f"Expected pcmb_dual, got {branch}"

    print("✓ Class 10 decision tree passed!")


def test_class_12_eligibility_and_recommendations():
    print("Testing Class 12 eligibility and recommendations...")

    # 1. BiPC student with programming interest (Prerequisite Gap)
    bipc_tech_answers = {
        "c12_stream": "BiPC",
        "c12_marks_level": "Above 75%",
        "c12_interest_level": "Very Interested",
        "c12_domain_choice": "Programming & Software Engineering (B.Tech CSE)",
        "c12_deep_dive": "I am eager to explore software and computers"
    }
    # Check eligibility directly
    res = check_pathway_eligibility("btech_cse", "BiPC")
    assert res["eligible"] is False
    assert res["is_prerequisite_gap"] is True
    assert "mandatory" in res["reason"] or "prerequisite" in res["reason"]

    # Generate full recs for BiPC
    bipc_recs = generate_class_12_recommendations("BiPC", bipc_tech_answers)
    top_names = [r["name"] for r in bipc_recs["top_recommendations"]]
    # B.Tech CSE must NOT be in top recommendations because it's ineligible!
    assert "B.Tech Computer Science & Engineering (CSE)" not in top_names
    assert len(bipc_recs["ineligible_alerts"]) > 0
    assert "B.Tech Computer Science & Engineering (CSE)" in bipc_recs["ineligible_alerts"][0]["name"]

    # 2. MPC Student with AI & Software interest
    mpc_ai_answers = {
        "c12_stream": "MPC",
        "c12_marks_level": "Above 75%",
        "c12_interest_level": "Very Interested",
        "c12_domain_choice": "Artificial Intelligence & Data Science",
        "c12_deep_dive": "Deep Learning, Neural Networks & Autonomous Systems"
    }
    mpc_recs = generate_class_12_recommendations("MPC", mpc_ai_answers)
    assert len(mpc_recs["top_recommendations"]) == 3
    assert mpc_recs["top_recommendations"][0]["id"] == "btech_aiml"
    assert mpc_recs["top_recommendations"][0]["match_score"] >= 90
    assert len(mpc_recs["ineligible_alerts"]) == 0

    # 3. Commerce Student with CA/Taxation interest
    comm_answers = {
        "c12_stream": "Commerce",
        "comm_has_math": "Yes, Commerce with Math",
        "c12_marks_level": "Above 75%",
        "c12_interest_level": "Very Interested",
        "c12_domain_choice": "Corporate Auditing, Accounting & Taxation (CA / CS / CMA)",
        "c12_deep_dive": "Auditing balance sheets, forensic accounting and tax strategy"
    }
    comm_recs = generate_class_12_recommendations("Commerce", comm_answers)
    assert len(comm_recs["top_recommendations"]) == 3
    assert comm_recs["top_recommendations"][0]["id"] in ["chartered_accountancy", "bcom_finance"]

    # 4. Humanities Student with Law interest
    hum_answers = {
        "c12_stream": "Humanities",
        "c12_marks_level": "Above 75%",
        "c12_interest_level": "Very Interested",
        "c12_domain_choice": "Legal Studies, Constitutional Law & Justice (BA LLB)",
        "c12_deep_dive": "Advocating for justice in courts, legal advisory & corporate law"
    }
    hum_recs = generate_class_12_recommendations("Humanities", hum_answers)
    assert len(hum_recs["top_recommendations"]) == 3
    assert hum_recs["top_recommendations"][0]["id"] == "integrated_law"

    print("✓ Class 12 eligibility and recommendations passed!")


def test_what_if_engine():
    print("Testing What-If counterfactual simulation engine...")
    from engine.what_if import (
        get_editable_answers_catalog, apply_what_if_update,
        generate_what_if_recommendations, compute_what_if_comparison
    )

    # 1. Test catalog generation for Class 12 MPC
    mpc_answers = {
        "entry_path": "class_12",
        "c12_stream": "MPC",
        "c12_marks_level": "Above 75%",
        "c12_interest_level": "Very Interested",
        "c12_domain_choice": "Programming & Software Engineering",
        "c12_deep_dive": "Cloud platforms, Web/Mobile apps & Enterprise software"
    }
    catalog = get_editable_answers_catalog(mpc_answers)
    assert len(catalog) >= 5
    keys = [item["key"] for item in catalog]
    assert "entry_path" in keys
    assert "c12_stream" in keys
    assert "c12_domain_choice" in keys

    # 2. Baseline recommendations
    base_recs = generate_what_if_recommendations(mpc_answers)
    assert base_recs["type"] == "class_12"
    assert len(base_recs["data"]["top_recommendations"]) == 3
    assert base_recs["data"]["top_recommendations"][0]["id"] == "btech_cse"

    # 3. Simulate What-If: Marks drop to Below 50%
    what_if_answers, notices = apply_what_if_update(mpc_answers, "c12_marks_level", "Below 50%")
    assert what_if_answers["c12_marks_level"] == "Below 50%"
    sim_recs = generate_what_if_recommendations(what_if_answers)
    comp = compute_what_if_comparison(base_recs, sim_recs, mpc_answers, what_if_answers)
    assert comp["is_modified"] is True
    assert len(comp["modifications"]) == 1
    cse_diff = next(p for p in comp["pathway_diffs"] if p["id"] == "btech_cse")
    # Reasons must reflect the academic performance shift
    assert "High academic performance (>75%) in core Class 12 subjects" in cse_diff["removed_reasons"]
    assert "Fulfills academic baseline requirements for university admissions" in cse_diff["added_reasons"]

    # Also test interest drop causing score drop
    what_if_interest, _ = apply_what_if_update(what_if_answers, "c12_interest_level", "Not Interested")
    sim_interest_recs = generate_what_if_recommendations(what_if_interest)
    comp_interest = compute_what_if_comparison(base_recs, sim_interest_recs, mpc_answers, what_if_interest)
    cse_int_diff = next(p for p in comp_interest["pathway_diffs"] if p["id"] == "btech_cse")
    assert cse_int_diff["score_delta"] < 0

    # 4. Simulate What-If: Stream change from MPC to BiPC (Eligibility constraint triggered)
    what_if_bipc, notices_bipc = apply_what_if_update(mpc_answers, "c12_stream", "BiPC")
    assert what_if_bipc["c12_stream"] == "BiPC"
    assert len(notices_bipc) > 0
    # Because original domain was Programming, it matched Programming & Software Engineering (B.Tech CSE)
    sim_bipc_recs = generate_what_if_recommendations(what_if_bipc)
    comp_bipc = compute_what_if_comparison(base_recs, sim_bipc_recs, mpc_answers, what_if_bipc)
    assert comp_bipc["is_modified"] is True
    # B.Tech CSE must become Ineligible!
    assert any(c["id"] == "btech_cse" and c["status_after"] == "Ineligible" for c in comp_bipc["eligibility_changes"])
    # Ineligible alerts should capture B.Tech CSE
    assert len(sim_bipc_recs["data"]["ineligible_alerts"]) > 0

    # 5. Simulate What-If: Class 10 profile shift
    c10_base = {
        "entry_path": "class_10",
        "math_marks": "above_75", "math_interest": "very_interested",
        "physics_marks": "above_75", "physics_interest": "very_interested",
        "chemistry_marks": "50_75", "chemistry_interest": "interested",
        "biology_marks": "below_50", "biology_interest": "not_interested",
        "social_marks": "below_50", "social_interest": "not_interested",
        "language_marks": "below_50", "language_interest": "neutral",
        "c10_adaptive_primary": "Programming and software",
        "c10_adaptive_followup": "Software & High-Tech Industry"
    }
    c10_base_recs = generate_what_if_recommendations(c10_base)
    assert c10_base_recs["streams"][0]["stream_id"] == "MPC"

    # Lower math and boost biology
    c10_sim, _ = apply_what_if_update(c10_base, "math_marks", "Below 50%")
    c10_sim, _ = apply_what_if_update(c10_sim, "math_interest", "Not Interested")
    c10_sim, _ = apply_what_if_update(c10_sim, "biology_marks", "Above 75%")
    c10_sim, _ = apply_what_if_update(c10_sim, "biology_interest", "Very Interested")
    c10_sim_recs = generate_what_if_recommendations(c10_sim)
    comp_c10 = compute_what_if_comparison(c10_base_recs, c10_sim_recs, c10_base, c10_sim)
    assert comp_c10["is_modified"] is True
    assert c10_sim_recs["streams"][0]["stream_id"] == "BiPC"
    assert any("Primary Recommended Stream changed" in h for h in comp_c10["highlights"])

    # 6. Simulate What-If: Stream change from BiPC to MPC (Eligibility granted)
    bipc_base_answers = {
        "entry_path": "class_12",
        "c12_stream": "BiPC",
        "c12_marks_level": "Above 75%",
        "c12_interest_level": "Very Interested",
        "c12_domain_choice": "Programming & Software Engineering (B.Tech CSE)",
        "c12_deep_dive": "I am eager to explore software and computers"
    }
    bipc_base_recs = generate_what_if_recommendations(bipc_base_answers)
    what_if_to_mpc, _ = apply_what_if_update(bipc_base_answers, "c12_stream", "MPC")
    mpc_sim_recs = generate_what_if_recommendations(what_if_to_mpc)
    comp_to_mpc = compute_what_if_comparison(bipc_base_recs, mpc_sim_recs, bipc_base_answers, what_if_to_mpc)
    assert any(c["id"] == "btech_cse" and c["status_after"] == "Eligible" for c in comp_to_mpc["eligibility_changes"])

    # 7. Simulate What-If: Cross-level switch (Class 10 -> Class 12)
    c10_to_12, notices_cross = apply_what_if_update(c10_base, "entry_path", "After Class 12")
    assert c10_to_12["entry_path"] == "class_12"
    assert "c12_stream" in c10_to_12
    assert len(notices_cross) > 0
    c12_from_10_recs = generate_what_if_recommendations(c10_to_12)
    comp_cross = compute_what_if_comparison(c10_base_recs, c12_from_10_recs, c10_base, c10_to_12)
    assert comp_cross["is_cross_level"] is True

    print("✓ What-If counterfactual simulation engine passed!")


if __name__ == "__main__":
    test_scoring_matrix()
    test_class_10_decision_tree()
    test_class_12_eligibility_and_recommendations()
    test_what_if_engine()
    print("\nALL TESTS PASSED SUCCESSFULLY!")

