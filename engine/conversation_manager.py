"""
Conversation Manager for state management, history tracking, and dynamic decision-tree routing.
Maintains Streamlit session state for Flo-like guided chat experience.
"""

import streamlit as st
from data.questions import (
    MASTER_QUESTION, CLASS_10_SUBJECT_QUESTIONS, MARKS_OPTIONS,
    INTEREST_OPTIONS, CLASS_10_ADAPTIVE_QUESTIONS, CLASS_12_STREAM_QUESTION,
    CLASS_12_STREAM_QUESTIONS
)
from data.rules import evaluate_class_10_branch, score_class_10_streams
from engine.scoring import compute_all_subject_scores
from engine.recommendation import generate_class_12_recommendations


def init_session_state():
    """
    Initializes all required session state variables.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "path" not in st.session_state:
        st.session_state.path = None  # 'class_10' or 'class_12'
    if "c10_subject_index" not in st.session_state:
        st.session_state.c10_subject_index = 0
    if "c10_sub_phase" not in st.session_state:
        st.session_state.c10_sub_phase = "marks"  # 'marks', 'interest', 'adaptive_primary', 'adaptive_followup'
    if "c10_adaptive_branch" not in st.session_state:
        st.session_state.c10_adaptive_branch = None
    if "c12_question_index" not in st.session_state:
        st.session_state.c12_question_index = 0
    if "is_complete" not in st.session_state:
        st.session_state.is_complete = False
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "what_if_answers" not in st.session_state:
        st.session_state.what_if_answers = None
    if "what_if_editing_key" not in st.session_state:
        st.session_state.what_if_editing_key = None
    if "what_if_notices" not in st.session_state:
        st.session_state.what_if_notices = []
    if "current_question" not in st.session_state:
        # Set initial master question
        st.session_state.current_question = MASTER_QUESTION
        st.session_state.chat_history.append({
            "sender": "bot",
            "text": MASTER_QUESTION["question"],
            "options": MASTER_QUESTION["options"],
            "id": MASTER_QUESTION["id"]
        })


def restart_assessment():
    """
    Resets all state to start a new assessment session from scratch.
    """
    st.session_state.chat_history = []
    st.session_state.answers = {}
    st.session_state.path = None
    st.session_state.c10_subject_index = 0
    st.session_state.c10_sub_phase = "marks"
    st.session_state.c10_adaptive_branch = None
    st.session_state.c12_question_index = 0
    st.session_state.is_complete = False
    st.session_state.recommendations = None
    st.session_state.what_if_answers = None
    st.session_state.what_if_editing_key = None
    st.session_state.what_if_notices = []
    
    st.session_state.current_question = MASTER_QUESTION
    st.session_state.chat_history.append({
        "sender": "bot",
        "text": MASTER_QUESTION["question"],
        "options": MASTER_QUESTION["options"],
        "id": MASTER_QUESTION["id"]
    })


def reset_what_if():
    """
    Restores the What-If simulation state to match the original assessment answers.
    """
    if "answers" in st.session_state and st.session_state.answers:
        st.session_state.what_if_answers = dict(st.session_state.answers)
    else:
        st.session_state.what_if_answers = None
    st.session_state.what_if_editing_key = None
    st.session_state.what_if_notices = []


def process_user_selection(selected_option: str):
    """
    Processes the selected button option, updates history & answers, and routes to the next question.
    """
    current_q = st.session_state.current_question
    if not current_q:
        return

    # 1. Append user message to chat history
    st.session_state.chat_history.append({
        "sender": "user",
        "text": selected_option
    })

    q_id = current_q["id"]

    # 2. Master entry question logic
    if q_id == "q_master_entry":
        if selected_option == "After Class 10":
            st.session_state.path = "class_10"
            st.session_state.answers["entry_path"] = "class_10"
            _load_next_class_10_question()
        else:
            st.session_state.path = "class_12"
            st.session_state.answers["entry_path"] = "class_12"
            _load_next_class_12_question()
        return

    # 3. Class 10 Path Logic
    if st.session_state.path == "class_10":
        _handle_class_10_selection(q_id, selected_option)
        return

    # 4. Class 12 Path Logic
    if st.session_state.path == "class_12":
        _handle_class_12_selection(q_id, selected_option)
        return


def _handle_class_10_selection(q_id: str, selected_option: str):
    idx = st.session_state.c10_subject_index
    sub_phase = st.session_state.c10_sub_phase

    # Standard Subject Loop (6 subjects: Marks + Interest)
    if idx < len(CLASS_10_SUBJECT_QUESTIONS):
        subj_info = CLASS_10_SUBJECT_QUESTIONS[idx]
        subj_id = subj_info["subject_id"]

        if sub_phase == "marks":
            val_map = {"Above 75%": "above_75", "50% to 75%": "50_75", "Below 50%": "below_50"}
            st.session_state.answers[f"{subj_id}_marks"] = val_map.get(selected_option, "below_50")
            st.session_state.c10_sub_phase = "interest"
            _load_next_class_10_question()
        elif sub_phase == "interest":
            val_map = {
                "Very Interested": "very_interested",
                "Interested": "interested",
                "Neutral": "neutral",
                "Not Interested": "not_interested"
            }
            st.session_state.answers[f"{subj_id}_interest"] = val_map.get(selected_option, "not_interested")
            st.session_state.c10_subject_index += 1
            st.session_state.c10_sub_phase = "marks"
            _load_next_class_10_question()
    elif sub_phase == "adaptive_primary":
        st.session_state.answers["c10_adaptive_primary"] = selected_option
        st.session_state.c10_sub_phase = "adaptive_followup"
        _load_next_class_10_question()
    elif sub_phase == "adaptive_followup":
        st.session_state.answers["c10_adaptive_followup"] = selected_option
        # Assessment complete -> calculate final recommendations
        st.session_state.is_complete = True
        st.session_state.current_question = None
        recs = score_class_10_streams(st.session_state.answers)
        subject_scores = compute_all_subject_scores(st.session_state.answers)
        st.session_state.recommendations = {
            "type": "class_10",
            "streams": recs,
            "subject_scores": subject_scores
        }
        st.session_state.chat_history.append({
            "sender": "bot",
            "text": "Thank you! I have analyzed your academic strengths and interest profile across all subjects. Below are your personalized Class 11 stream recommendations.",
            "options": []
        })


def _load_next_class_10_question():
    idx = st.session_state.c10_subject_index
    sub_phase = st.session_state.c10_sub_phase

    if idx < len(CLASS_10_SUBJECT_QUESTIONS):
        subj_info = CLASS_10_SUBJECT_QUESTIONS[idx]
        if sub_phase == "marks":
            next_q = {
                "id": subj_info["marks_q_id"],
                "question": f"[{idx+1}/{len(CLASS_10_SUBJECT_QUESTIONS)}] {subj_info['marks_question']}",
                "options": [o["label"] for o in MARKS_OPTIONS]
            }
        else:
            next_q = {
                "id": subj_info["interest_q_id"],
                "question": f"[{idx+1}/{len(CLASS_10_SUBJECT_QUESTIONS)}] {subj_info['interest_question']}",
                "options": [o["label"] for o in INTEREST_OPTIONS]
            }
    elif sub_phase == "marks" or sub_phase == "adaptive_primary":
        # First time entering adaptive branch
        st.session_state.c10_sub_phase = "adaptive_primary"
        branch = evaluate_class_10_branch(st.session_state.answers)
        st.session_state.c10_adaptive_branch = branch
        branch_data = CLASS_10_ADAPTIVE_QUESTIONS.get(branch, CLASS_10_ADAPTIVE_QUESTIONS["mpc_tech"])
        primary_q = branch_data["primary"]
        next_q = {
            "id": primary_q["id"],
            "question": primary_q["question"],
            "options": primary_q["options"]
        }
    elif sub_phase == "adaptive_followup":
        branch = st.session_state.c10_adaptive_branch or evaluate_class_10_branch(st.session_state.answers)
        branch_data = CLASS_10_ADAPTIVE_QUESTIONS.get(branch, CLASS_10_ADAPTIVE_QUESTIONS["mpc_tech"])
        followup_q = branch_data["follow_up"]
        next_q = {
            "id": followup_q["id"],
            "question": followup_q["question"],
            "options": followup_q["options"]
        }

    st.session_state.current_question = next_q
    st.session_state.chat_history.append({
        "sender": "bot",
        "text": next_q["question"],
        "options": next_q["options"],
        "id": next_q["id"]
    })


def _handle_class_12_selection(q_id: str, selected_option: str):
    if q_id == "q_c12_stream":
        st.session_state.answers["c12_stream"] = selected_option
        st.session_state.c12_question_index = 0
        _load_next_class_12_question()
        return

    stream = st.session_state.answers.get("c12_stream", "MPC")
    q_list = CLASS_12_STREAM_QUESTIONS.get(stream, [])
    idx = st.session_state.c12_question_index

    if idx < len(q_list):
        q_data = q_list[idx]
        key = q_data["key"]
        st.session_state.answers[key] = selected_option
        st.session_state.c12_question_index += 1
        _load_next_class_12_question()


def _load_next_class_12_question():
    if "c12_stream" not in st.session_state.answers:
        next_q = CLASS_12_STREAM_QUESTION
    else:
        stream = st.session_state.answers["c12_stream"]
        q_list = CLASS_12_STREAM_QUESTIONS.get(stream, [])
        idx = st.session_state.c12_question_index

        if idx < len(q_list):
            q_data = q_list[idx]
            next_q = {
                "id": q_data["id"],
                "question": f"[{idx+1}/{len(q_list)}] {q_data['question']}",
                "options": q_data["options"]
            }
        else:
            # Assessment complete -> calculate final recommendations
            st.session_state.is_complete = True
            st.session_state.current_question = None
            recs = generate_class_12_recommendations(stream, st.session_state.answers)
            st.session_state.recommendations = {
                "type": "class_12",
                "stream": stream,
                "data": recs
            }
            st.session_state.chat_history.append({
                "sender": "bot",
                "text": f"Assessment complete for Class 12 ({stream}). Here are your top career and degree recommendations based on academic eligibility and rule matrix scoring.",
                "options": []
            })
            return

    st.session_state.current_question = next_q
    st.session_state.chat_history.append({
        "sender": "bot",
        "text": next_q["question"],
        "options": next_q["options"],
        "id": next_q["id"]
    })


def calculate_progress_percentage() -> int:
    """
    Returns progress percentage (0 - 100) based on current state.
    """
    if st.session_state.is_complete:
        return 100
    if not st.session_state.path:
        return 5

    if st.session_state.path == "class_10":
        # Total steps = 6 subjects * 2 (12) + 2 adaptive (2) + 1 entry = 15
        done_steps = 1 + (st.session_state.c10_subject_index * 2)
        if st.session_state.c10_sub_phase == "interest":
            done_steps += 1
        elif st.session_state.c10_sub_phase == "adaptive_primary":
            done_steps = 13
        elif st.session_state.c10_sub_phase == "adaptive_followup":
            done_steps = 14
        return min(95, int((done_steps / 15) * 100))
    else:
        # Class 12 path: 1 entry + 1 stream + len(q_list)
        stream = st.session_state.answers.get("c12_stream")
        if not stream:
            return 15
        total_q = len(CLASS_12_STREAM_QUESTIONS.get(stream, [1, 2, 3, 4])) + 2
        done_steps = 2 + st.session_state.c12_question_index
        return min(95, int((done_steps / total_q) * 100))
