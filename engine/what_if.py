"""
What-If / Counterfactual Simulation Engine.
Enables students and counsellors to modify prior answers, simulate alternative
academic/interest scenarios, and inspect deterministic recommendation shifts,
rank movements, eligibility constraints, and scoring rationale differences.
Strictly deterministic without any AI/ML dependencies.
"""

from data.questions import (
    MASTER_QUESTION, CLASS_10_SUBJECT_QUESTIONS, MARKS_OPTIONS,
    INTEREST_OPTIONS, CLASS_10_ADAPTIVE_QUESTIONS, CLASS_12_STREAM_QUESTION,
    CLASS_12_STREAM_QUESTIONS
)
from data.careers import CAREERS_DB
from data.rules import evaluate_class_10_branch, score_class_10_streams
from engine.scoring import (
    compute_all_subject_scores, MARKS_DISPLAY, INTEREST_DISPLAY
)
from engine.eligibility import check_pathway_eligibility
from engine.recommendation import generate_class_12_recommendations, STREAM_PATHWAY_MAP


DISPLAY_TO_MARKS = {v: k for k, v in MARKS_DISPLAY.items()}
DISPLAY_TO_INTEREST = {v: k for k, v in INTEREST_DISPLAY.items()}

BRANCH_TITLES = {
    "mpc_tech": "Mathematics & Physical Sciences (Engineering / Tech)",
    "bipc_health": "Biology & Chemical Sciences (Medical / Healthcare)",
    "pcmb_dual": "Interdisciplinary Dual Science (Math + Biology)",
    "social_lang": "Social Sciences, Law & Humanities",
    "commerce_general": "Commerce, Finance & Business Management"
}


def get_editable_answers_catalog(answers: dict) -> list[dict]:
    """
    Returns a structured catalog of all active answers given by the user,
    with prompts, options, friendly display labels, and categories.
    """
    catalog = []
    entry_path = answers.get("entry_path", "class_12")

    # 1. Guidance Level / Entry Question
    catalog.append({
        "key": "entry_path",
        "category": "Guidance Level",
        "title": "Assessment Level",
        "prompt": MASTER_QUESTION["question"],
        "options": MASTER_QUESTION["options"],
        "current_raw": entry_path,
        "current_display": "After Class 10" if entry_path == "class_10" else "After Class 12"
    })

    if entry_path == "class_10":
        # Subject Marks and Interests (6 subjects)
        for subj in CLASS_10_SUBJECT_QUESTIONS:
            s_id = subj["subject_id"]
            s_name = subj["name"]

            # Marks
            m_key = f"{s_id}_marks"
            m_val = answers.get(m_key, "below_50")
            catalog.append({
                "key": m_key,
                "category": "Class 10 Academic Performance",
                "title": f"{s_name} Marks",
                "prompt": subj["marks_question"],
                "options": [o["label"] for o in MARKS_OPTIONS],
                "current_raw": m_val,
                "current_display": MARKS_DISPLAY.get(m_val, m_val)
            })

            # Interest
            i_key = f"{s_id}_interest"
            i_val = answers.get(i_key, "not_interested")
            catalog.append({
                "key": i_key,
                "category": "Class 10 Subject Interest",
                "title": f"{s_name} Passion / Interest",
                "prompt": subj["interest_question"],
                "options": [o["label"] for o in INTEREST_OPTIONS],
                "current_raw": i_val,
                "current_display": INTEREST_DISPLAY.get(i_val, i_val)
            })

        # Adaptive Questions based on current branch
        branch = evaluate_class_10_branch(answers)
        branch_data = CLASS_10_ADAPTIVE_QUESTIONS.get(branch, CLASS_10_ADAPTIVE_QUESTIONS["mpc_tech"])

        p_val = answers.get("c10_adaptive_primary", branch_data["primary"]["options"][0])
        catalog.append({
            "key": "c10_adaptive_primary",
            "category": "Class 10 Adaptive Specialization",
            "title": "Primary Domain Orientation",
            "prompt": branch_data["primary"]["question"],
            "options": branch_data["primary"]["options"],
            "current_raw": p_val,
            "current_display": p_val
        })

        f_val = answers.get("c10_adaptive_followup", branch_data["follow_up"]["options"][0])
        catalog.append({
            "key": "c10_adaptive_followup",
            "category": "Class 10 Career Horizon",
            "title": "Target Environment / Horizon",
            "prompt": branch_data["follow_up"]["question"],
            "options": branch_data["follow_up"]["options"],
            "current_raw": f_val,
            "current_display": f_val
        })

    else:
        # Class 12 Path
        stream = answers.get("c12_stream", "MPC")
        catalog.append({
            "key": "c12_stream",
            "category": "Class 12 Academic Background",
            "title": "Academic Stream",
            "prompt": CLASS_12_STREAM_QUESTION["question"],
            "options": CLASS_12_STREAM_QUESTION["options"],
            "current_raw": stream,
            "current_display": stream
        })

        q_list = CLASS_12_STREAM_QUESTIONS.get(stream, [])
        for q in q_list:
            key = q["key"]
            val = answers.get(key, q["options"][0] if q.get("options") else "")
            
            title_map = {
                "c12_marks_level": "Academic Performance Range",
                "c12_interest_level": "Subject Passion & Aptitude",
                "c12_domain_choice": "Preferred Career Domain",
                "c12_deep_dive": "Professional Specialization",
                "comm_has_math": "Class 12 Mathematics Background",
                "pcmb_pref": "Primary Science Orientation"
            }
            title = title_map.get(key, key.replace("c12_", "").replace("_", " ").title())

            cat_map = {
                "c12_marks_level": "Class 12 Academic Performance",
                "c12_interest_level": "Class 12 Interest & Aptitude",
                "c12_domain_choice": "Class 12 Domain Orientation",
                "c12_deep_dive": "Class 12 Specialization Focus",
                "comm_has_math": "Class 12 Subject Prerequisites",
                "pcmb_pref": "Class 12 Dual-Science Preference"
            }
            category = cat_map.get(key, "Class 12 Specialization")

            catalog.append({
                "key": key,
                "category": category,
                "title": title,
                "prompt": q["question"],
                "options": q["options"],
                "current_raw": val,
                "current_display": val
            })

    return catalog


def apply_what_if_update(what_if_answers: dict, key: str, selected_option_label: str) -> tuple[dict, list[str]]:
    """
    Applies a user-selected change to what_if_answers, handling data conversion
    and cascading dependencies (e.g. stream changes or entry_path changes).
    
    Returns:
    - updated_answers: dict
    - notices: list[str] (warnings or informative messages for edge cases)
    """
    updated = dict(what_if_answers)
    notices = []

    # 1. Master Guidance Level Switch (Class 10 <-> Class 12)
    if key == "entry_path":
        new_path = "class_10" if "10" in selected_option_label else "class_12"
        old_path = updated.get("entry_path", "")
        updated["entry_path"] = new_path

        if new_path != old_path:
            if new_path == "class_10":
                # Ensure Class 10 keys exist
                subjects = ["math", "physics", "chemistry", "biology", "social", "language"]
                for s in subjects:
                    if f"{s}_marks" not in updated:
                        updated[f"{s}_marks"] = "above_75"
                    if f"{s}_interest" not in updated:
                        updated[f"{s}_interest"] = "very_interested"
                branch = evaluate_class_10_branch(updated)
                bdata = CLASS_10_ADAPTIVE_QUESTIONS.get(branch, CLASS_10_ADAPTIVE_QUESTIONS["mpc_tech"])
                updated["c10_adaptive_primary"] = bdata["primary"]["options"][0]
                updated["c10_adaptive_followup"] = bdata["follow_up"]["options"][0]
                notices.append(
                    "Switched guidance level from Class 12 to Class 10. Default academic profile loaded. "
                    "You can now customize subject marks and interests below."
                )
            else:
                # Ensure Class 12 keys exist
                if "c12_stream" not in updated:
                    updated["c12_stream"] = "MPC"
                stream = updated["c12_stream"]
                q_list = CLASS_12_STREAM_QUESTIONS.get(stream, [])
                for q in q_list:
                    k = q["key"]
                    if k not in updated:
                        updated[k] = q["options"][0]
                notices.append(
                    f"Switched guidance level from Class 10 to Class 12 ({stream}). "
                    "Default Class 12 options loaded. Customize your stream and domain choices below."
                )
        return updated, notices

    # 2. Class 12 Stream Switch
    if key == "c12_stream":
        old_stream = updated.get("c12_stream", "")
        new_stream = selected_option_label
        updated["c12_stream"] = new_stream

        if new_stream != old_stream:
            new_q_list = CLASS_12_STREAM_QUESTIONS.get(new_stream, [])
            valid_keys = {q["key"]: q["options"] for q in new_q_list}

            # Adjust domain choice to match new stream options
            old_domain = updated.get("c12_domain_choice", "")
            if "c12_domain_choice" in valid_keys:
                allowed_domains = valid_keys["c12_domain_choice"]
                # Try finding closest match (e.g. "Programming" -> BiPC's "Programming & Software Engineering (B.Tech CSE)")
                matched = None
                for opt in allowed_domains:
                    if any(w.lower() in opt.lower() for w in old_domain.split() if len(w) > 4):
                        matched = opt
                        break
                updated["c12_domain_choice"] = matched if matched else allowed_domains[0]

            # Adjust deep dive
            old_deep_dive = updated.get("c12_deep_dive", "")
            if "c12_deep_dive" in valid_keys:
                allowed_dd = valid_keys["c12_deep_dive"]
                matched_dd = None
                for opt in allowed_dd:
                    if any(w.lower() in opt.lower() for w in old_deep_dive.split() if len(w) > 4):
                        matched_dd = opt
                        break
                updated["c12_deep_dive"] = matched_dd if matched_dd else allowed_dd[0]

            # Stream-specific keys
            if new_stream == "Commerce":
                if "comm_has_math" not in updated:
                    updated["comm_has_math"] = "Yes, Commerce with Math"
            else:
                updated.pop("comm_has_math", None)

            if new_stream == "PCMB":
                if "pcmb_pref" not in updated:
                    updated["pcmb_pref"] = "Engineering and Technology (Tech Focus)"
            else:
                updated.pop("pcmb_pref", None)

            # Ensure marks and interest are valid
            if "c12_marks_level" not in updated:
                updated["c12_marks_level"] = "Above 75%"
            if new_stream != "PCMB" and "c12_interest_level" not in updated:
                updated["c12_interest_level"] = "Very Interested"

            notices.append(
                f"Class 12 Stream updated from {old_stream} to {new_stream}. "
                "Dependent question options for domain and specialization have been aligned with the new stream."
            )
        return updated, notices

    # 3. Class 10 Subject Marks
    if key.endswith("_marks") and key != "c12_marks_level":
        raw_val = DISPLAY_TO_MARKS.get(selected_option_label, "below_50")
        updated[key] = raw_val

        # Check if adaptive branch changed
        old_branch = evaluate_class_10_branch(what_if_answers)
        new_branch = evaluate_class_10_branch(updated)
        if new_branch != old_branch:
            bdata = CLASS_10_ADAPTIVE_QUESTIONS.get(new_branch, CLASS_10_ADAPTIVE_QUESTIONS["mpc_tech"])
            updated["c10_adaptive_primary"] = bdata["primary"]["options"][0]
            updated["c10_adaptive_followup"] = bdata["follow_up"]["options"][0]
            notices.append(
                f"Subject score adjustment shifted your adaptive branch to "
                f"'{BRANCH_TITLES.get(new_branch, new_branch)}'. Adaptive questions have been refreshed."
            )
        return updated, notices

    # 4. Class 10 Subject Interest
    if key.endswith("_interest") and key != "c12_interest_level":
        raw_val = DISPLAY_TO_INTEREST.get(selected_option_label, "not_interested")
        updated[key] = raw_val

        # Check if adaptive branch changed
        old_branch = evaluate_class_10_branch(what_if_answers)
        new_branch = evaluate_class_10_branch(updated)
        if new_branch != old_branch:
            bdata = CLASS_10_ADAPTIVE_QUESTIONS.get(new_branch, CLASS_10_ADAPTIVE_QUESTIONS["mpc_tech"])
            updated["c10_adaptive_primary"] = bdata["primary"]["options"][0]
            updated["c10_adaptive_followup"] = bdata["follow_up"]["options"][0]
            notices.append(
                f"Subject passion adjustment shifted your adaptive branch to "
                f"'{BRANCH_TITLES.get(new_branch, new_branch)}'. Adaptive questions have been refreshed."
            )
        return updated, notices

    # 5. Direct value assignment (Class 12 questions, Class 10 adaptive questions)
    updated[key] = selected_option_label
    return updated, notices


def generate_what_if_recommendations(what_if_answers: dict) -> dict:
    """
    Deterministically re-runs the recommendation engine using modified answers.
    Reuses existing scoring and recommendation functions without modification.
    """
    entry_path = what_if_answers.get("entry_path", "class_12")

    if entry_path == "class_10":
        recs = score_class_10_streams(what_if_answers)
        subject_scores = compute_all_subject_scores(what_if_answers)
        return {
            "type": "class_10",
            "streams": recs,
            "subject_scores": subject_scores
        }
    else:
        stream = what_if_answers.get("c12_stream", "MPC")
        recs = generate_class_12_recommendations(stream, what_if_answers)
        return {
            "type": "class_12",
            "stream": stream,
            "data": recs
        }


def compute_what_if_comparison(
    original_rec: dict,
    what_if_rec: dict,
    original_answers: dict,
    what_if_answers: dict
) -> dict:
    """
    Computes a comprehensive diff between original assessment results and what-if simulation:
    - Answer modifications (which answers changed)
    - Summary highlight points (e.g. rank changes, eligibility triggers)
    - Side-by-side pathway / stream comparisons
    - Eligibility status shifts
    - Score deltas
    - Key reasons added or removed
    """
    orig_type = original_rec.get("type", "class_12")
    new_type = what_if_rec.get("type", "class_12")

    # 1. Answer Modifications List
    modifications = []
    catalog_orig = {item["key"]: item for item in get_editable_answers_catalog(original_answers)}
    catalog_new = {item["key"]: item for item in get_editable_answers_catalog(what_if_answers)}

    for key, new_item in catalog_new.items():
        if key in catalog_orig:
            orig_item = catalog_orig[key]
            if orig_item["current_raw"] != new_item["current_raw"]:
                modifications.append({
                    "key": key,
                    "title": new_item["title"],
                    "category": new_item["category"],
                    "original_display": orig_item["current_display"],
                    "what_if_display": new_item["current_display"]
                })

    is_modified = len(modifications) > 0
    highlights = []
    eligibility_changes = []

    # Handle Cross-Level Transition (Class 10 <-> Class 12)
    if orig_type != new_type:
        highlights.append(
            f"Guidance Assessment Level changed from {'Class 10' if orig_type == 'class_10' else 'Class 12'} "
            f"to {'Class 10' if new_type == 'class_10' else 'Class 12'}."
        )
        return {
            "is_modified": is_modified,
            "is_cross_level": True,
            "modifications": modifications,
            "highlights": highlights,
            "orig_type": orig_type,
            "new_type": new_type,
            "original_rec": original_rec,
            "what_if_rec": what_if_rec,
            "eligibility_changes": []
        }

    # -------------------------------------------------------------
    # CLASS 12 COMPARISON
    # -------------------------------------------------------------
    if orig_type == "class_12":
        orig_stream = original_rec.get("stream", "")
        new_stream = what_if_rec.get("stream", "")

        if orig_stream != new_stream:
            highlights.append(f"Class 12 Academic Stream changed: **{orig_stream}** ➔ **{new_stream}**")

        orig_top = original_rec["data"]["top_recommendations"]
        new_top = what_if_rec["data"]["top_recommendations"]

        orig_top_map = {r["id"]: (idx + 1, r) for idx, r in enumerate(orig_top)}
        new_top_map = {r["id"]: (idx + 1, r) for idx, r in enumerate(new_top)}

        # Detect Rank #1 change
        if orig_top and new_top:
            if orig_top[0]["id"] != new_top[0]["id"]:
                highlights.append(
                    f"Top Recommended Pathway changed from **{orig_top[0]['name']}** ({orig_top[0]['match_score']}%) "
                    f"to **{new_top[0]['name']}** ({new_top[0]['match_score']}%)"
                )

        # Detect rank shifts among top recommendations
        for pid, (new_rank, new_item) in new_top_map.items():
            if pid in orig_top_map:
                orig_rank, orig_item = orig_top_map[pid]
                score_delta = new_item["match_score"] - orig_item["match_score"]
                if orig_rank != new_rank:
                    sign = "+" if score_delta > 0 else ""
                    delta_str = f" ({sign}{score_delta}%)" if score_delta != 0 else ""
                    highlights.append(
                        f"**{new_item['name']}** moved from **Rank {orig_rank}** ➔ **Rank {new_rank}**{delta_str}"
                    )
                elif score_delta != 0:
                    sign = "+" if score_delta > 0 else ""
                    highlights.append(
                        f"**{new_item['name']}** score updated: {orig_item['match_score']}% ➔ {new_item['match_score']}% ({sign}{score_delta}%)"
                    )
            else:
                highlights.append(
                    f"**{new_item['name']}** entered Top Recommendations at **Rank {new_rank}** ({new_item['match_score']}% Match)"
                )

        for pid, (orig_rank, orig_item) in orig_top_map.items():
            if pid not in new_top_map:
                highlights.append(
                    f"**{orig_item['name']}** (was Rank {orig_rank}, {orig_item['match_score']}%) dropped out of Top 3"
                )

        # Detect Eligibility Status Changes
        # Check all candidate pathways across both streams
        all_candidates = set(STREAM_PATHWAY_MAP.get(orig_stream, [])) | set(STREAM_PATHWAY_MAP.get(new_stream, []))
        for pid in all_candidates:
            p_info = CAREERS_DB.get(pid, {})
            p_name = p_info.get("name", pid)
            orig_elig = check_pathway_eligibility(pid, orig_stream, original_answers)
            new_elig = check_pathway_eligibility(pid, new_stream, what_if_answers)

            if orig_elig["eligible"] and not new_elig["eligible"]:
                eligibility_changes.append({
                    "id": pid,
                    "name": p_name,
                    "status_before": "Eligible",
                    "status_after": "Ineligible",
                    "reason": new_elig["reason"],
                    "suggested_alternatives": new_elig.get("suggested_alternatives", [])
                })
                highlights.append(
                    f"**{p_name}** became INELIGIBLE ({new_elig['reason'].split('.')[0]}.)"
                )
            elif not orig_elig["eligible"] and new_elig["eligible"]:
                eligibility_changes.append({
                    "id": pid,
                    "name": p_name,
                    "status_before": "Ineligible",
                    "status_after": "Eligible",
                    "reason": "Satisfies prerequisites under current stream.",
                    "suggested_alternatives": []
                })
                highlights.append(f"**{p_name}** became ELIGIBLE under {new_stream} stream")

        # Ineligible alerts before and after
        inelig_alerts_before = original_rec["data"].get("ineligible_alerts", [])
        inelig_alerts_after = what_if_rec["data"].get("ineligible_alerts", [])

        # Build detailed pathway comparison items
        pathway_diffs = []
        all_top_ids = list(dict.fromkeys(
            [r["id"] for r in orig_top] + [r["id"] for r in new_top]
        ))

        for pid in all_top_ids:
            p_info = CAREERS_DB.get(pid, {})
            name = p_info.get("name", pid)
            
            orig_item = orig_top_map.get(pid, (None, None))[1]
            new_item = new_top_map.get(pid, (None, None))[1]

            rank_before = orig_top_map.get(pid, (None, None))[0]
            rank_after = new_top_map.get(pid, (None, None))[0]

            score_before = orig_item["match_score"] if orig_item else None
            score_after = new_item["match_score"] if new_item else None
            score_delta = (score_after - score_before) if (score_after is not None and score_before is not None) else None

            reasons_before = orig_item.get("reasons", []) if orig_item else []
            reasons_after = new_item.get("reasons", []) if new_item else []

            added_reasons = [r for r in reasons_after if r not in reasons_before]
            removed_reasons = [r for r in reasons_before if r not in reasons_after]

            pathway_diffs.append({
                "id": pid,
                "name": name,
                "rank_before": rank_before,
                "rank_after": rank_after,
                "score_before": score_before,
                "score_after": score_after,
                "score_delta": score_delta,
                "reasons_before": reasons_before,
                "reasons_after": reasons_after,
                "added_reasons": added_reasons,
                "removed_reasons": removed_reasons,
                "orig_item": orig_item,
                "new_item": new_item
            })

        return {
            "is_modified": is_modified,
            "is_cross_level": False,
            "orig_type": "class_12",
            "new_type": "class_12",
            "modifications": modifications,
            "highlights": highlights,
            "pathway_diffs": pathway_diffs,
            "eligibility_changes": eligibility_changes,
            "ineligible_alerts_before": inelig_alerts_before,
            "ineligible_alerts_after": inelig_alerts_after,
            "top_before": orig_top,
            "top_after": new_top
        }

    # -------------------------------------------------------------
    # CLASS 10 COMPARISON
    # -------------------------------------------------------------
    else:
        orig_streams = original_rec["streams"]
        new_streams = what_if_rec["streams"]

        orig_stream_map = {s["stream_id"]: (idx + 1, s) for idx, s in enumerate(orig_streams)}
        new_stream_map = {s["stream_id"]: (idx + 1, s) for idx, s in enumerate(new_streams)}

        # Check Top stream change
        if orig_streams and new_streams:
            if orig_streams[0]["stream_id"] != new_streams[0]["stream_id"]:
                highlights.append(
                    f"Primary Recommended Stream changed from **{orig_streams[0]['name']}** ({orig_streams[0]['match_score']}%) "
                    f"to **{new_streams[0]['name']}** ({new_streams[0]['match_score']}%)"
                )

        # Check stream rank and score changes
        stream_diffs = []
        for s_id, (new_rank, new_item) in new_stream_map.items():
            orig_rank, orig_item = orig_stream_map.get(s_id, (None, None))
            score_before = orig_item["match_score"] if orig_item else None
            score_after = new_item["match_score"]
            score_delta = score_after - score_before if score_before is not None else 0

            if orig_rank != new_rank:
                sign = "+" if score_delta > 0 else ""
                highlights.append(
                    f"**{new_item['name']}** moved from **Rank {orig_rank}** ➔ **Rank {new_rank}** ({score_before}% ➔ {score_after}%, {sign}{score_delta}%)"
                )
            elif score_delta != 0:
                sign = "+" if score_delta > 0 else ""
                highlights.append(
                    f"**{new_item['name']}** match score shifted by {sign}{score_delta}% ({score_before}% ➔ {score_after}%)"
                )

            reasons_before = orig_item.get("reasons", []) if orig_item else []
            reasons_after = new_item.get("reasons", [])

            added_reasons = [r for r in reasons_after if r not in reasons_before]
            removed_reasons = [r for r in reasons_before if r not in reasons_after]

            stream_diffs.append({
                "stream_id": s_id,
                "name": new_item["name"],
                "rank_before": orig_rank,
                "rank_after": new_rank,
                "score_before": score_before,
                "score_after": score_after,
                "score_delta": score_delta,
                "reasons_before": reasons_before,
                "reasons_after": reasons_after,
                "added_reasons": added_reasons,
                "removed_reasons": removed_reasons,
                "orig_item": orig_item,
                "new_item": new_item
            })

        # Subject score differences
        subj_labels = {
            "math_score": "Mathematics",
            "physics_score": "Physics",
            "chemistry_score": "Chemistry",
            "biology_score": "Biology",
            "social_score": "Social Studies",
            "language_score": "Language & Literature"
        }
        subj_diffs = []
        orig_scores = original_rec.get("subject_scores", {})
        new_scores = what_if_rec.get("subject_scores", {})

        for k, label in subj_labels.items():
            sb = orig_scores.get(k, 0)
            sa = new_scores.get(k, 0)
            delta = sa - sb
            if delta != 0:
                sign = "+" if delta > 0 else ""
                highlights.append(f"{label} performance score shifted: {sb}/10 ➔ {sa}/10 ({sign}{delta})")
            subj_diffs.append({
                "subject": label,
                "score_before": sb,
                "score_after": sa,
                "score_delta": delta
            })

        return {
            "is_modified": is_modified,
            "is_cross_level": False,
            "orig_type": "class_10",
            "new_type": "class_10",
            "modifications": modifications,
            "highlights": highlights,
            "stream_diffs": stream_diffs,
            "subject_diffs": subj_diffs,
            "orig_streams": orig_streams,
            "new_streams": new_streams
        }
