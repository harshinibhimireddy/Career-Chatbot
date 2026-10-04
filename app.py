"""
Streamlit Web Application for Rule-Based Career Recommendation Chatbot.
Executive, modern enterprise UI for Indian student career guidance.
Strictly deterministic without any AI/ML dependencies.
"""

import time
import streamlit as st
import streamlit.components.v1 as components
from engine.conversation_manager import (
    init_session_state, process_user_selection, restart_assessment,
    calculate_progress_percentage, reset_what_if
)
from engine.what_if import (
    get_editable_answers_catalog, apply_what_if_update,
    generate_what_if_recommendations, compute_what_if_comparison
)

# Page configuration
st.set_page_config(
    page_title="Career Guidance Platform",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Bespoke Editorial Dark Theme with Black & Good Orange Palette
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">

<style>
    /* Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background-color: #0B0B0B !important;
        color: #EDEDED !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Headings in Editorial Serif */
    h1, h2, h3, h4, .brand-title, .rec-title, .banner-title {
        font-family: 'Lora', 'Merriweather', 'Georgia', serif !important;
        font-weight: 600;
        letter-spacing: -0.01em;
    }

    /* Streamlit Main Viewport */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 860px;
    }

    /* Brand Header */
    .brand-header {
        text-align: center;
        padding: 12px 0 26px 0;
        border-bottom: 1px solid #222222;
        margin-bottom: 26px;
    }
    .brand-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #FB923C;
        background-color: #1F140D;
        border: 1px solid #5C280C;
        padding: 4px 14px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    .brand-title {
        font-size: 2.3rem;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.25;
    }
    .brand-subtitle {
        color: #A3A3A3;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 8px;
    }

    /* Sticky Progress Bar Area */
    div.stElementContainer:has(#section-progress),
    div.stElementContainer:has(.sticky-progress-container) {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 2.85rem !important;
        z-index: 995 !important;
    }
    .sticky-progress-container {
        position: -webkit-sticky;
        position: sticky;
        top: 2.85rem;
        z-index: 995;
        background-color: rgba(11, 11, 11, 0.95);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid #242424;
        border-top: 1px solid #333333;
        border-radius: 8px;
        padding: 12px 18px 14px 18px;
        margin-bottom: 24px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.7);
        transition: border-color 0.2s ease;
    }
    .sticky-progress-inner {
        width: 100%;
    }
    .sticky-progress-label-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .sticky-progress-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #A3A3A3;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .sticky-progress-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #EA580C;
        display: inline-block;
        box-shadow: 0 0 8px rgba(234, 88, 12, 0.6);
    }
    .sticky-progress-val {
        font-size: 0.82rem;
        font-weight: 700;
        color: #FB923C;
        font-family: 'Inter', monospace, sans-serif;
        letter-spacing: 0.04em;
    }
    .sticky-progress-track {
        width: 100%;
        height: 7px;
        background-color: #1A1A1A;
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #2A2A2A;
    }
    .sticky-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #C2410C 0%, #EA580C 60%, #FB923C 100%);
        border-radius: 4px;
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Section Anchors & Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    .section-anchor,
    #section-progress,
    #section-assessment,
    #section-recommendations,
    #section-evaluation,
    #section-prerequisites,
    #section-whatif {
        scroll-margin-top: 5.5rem;
    }

    @keyframes sectionPulse {
        0% { outline: 2px solid transparent; box-shadow: 0 0 0 rgba(234, 88, 12, 0); }
        30% { outline: 2px solid #EA580C; box-shadow: 0 0 18px rgba(234, 88, 12, 0.45); }
        100% { outline: 2px solid transparent; box-shadow: 0 0 0 rgba(234, 88, 12, 0); }
    }
    .section-highlight {
        animation: sectionPulse 1.8s ease;
        border-radius: 8px;
    }

    /* Sidebar Feature Navigation Cards */
    .sidebar-section-title {
        font-family: 'Lora', 'Merriweather', 'Georgia', serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: #EDEDED;
        margin: 16px 0 6px 0;
        letter-spacing: 0.01em;
    }
    .sidebar-section-subtitle {
        font-size: 0.76rem;
        color: #737373;
        margin-bottom: 12px;
        line-height: 1.35;
    }
    .sidebar-features-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 18px;
    }
    .sidebar-feature-card {
        display: block;
        text-decoration: none !important;
        background-color: #121212;
        border: 1px solid #242424;
        border-left: 3px solid #333333;
        border-radius: 6px;
        padding: 9px 12px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .sidebar-feature-card:hover {
        background-color: #1A1410;
        border-color: #382415;
        border-left: 3px solid #EA580C;
        transform: translateX(2px);
    }
    .sidebar-feature-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    .sidebar-feature-title {
        font-size: 0.80rem;
        font-weight: 600;
        color: #EDEDED;
        letter-spacing: 0.01em;
    }
    .sidebar-feature-tag {
        font-size: 0.63rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 2px 6px;
        border-radius: 3px;
        background-color: #1F140D;
        color: #FB923C;
        border: 1px solid #431E0C;
    }
    .sidebar-feature-tag.tag-locked {
        background-color: #181818;
        color: #666666;
        border-color: #282828;
    }
    .sidebar-feature-desc {
        font-size: 0.72rem;
        color: #909090;
        line-height: 1.35;
        margin-bottom: 5px;
    }
    .sidebar-feature-cta {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 0.68rem;
        font-weight: 600;
        color: #EA580C;
        letter-spacing: 0.03em;
    }

    /* Chat Stream Layout */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        gap: 14px;
        margin-bottom: 24px;
        width: 100%;
    }

    /* Bot Message Bubble */
    .bot-row {
        display: flex;
        justify-content: flex-start;
        width: 100%;
    }
    .bot-bubble {
        display: inline-block;
        max-width: 84%;
        background-color: #141414;
        border: 1px solid #262626;
        color: #EDEDED;
        padding: 16px 22px;
        border-radius: 12px 12px 12px 2px;
        line-height: 1.55;
        font-size: 0.95rem;
        font-weight: 400;
        word-wrap: break-word;
    }

    /* User Bubble (Right-aligned, deep warm orange) */
    .user-row {
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }
    .user-bubble {
        display: inline-block;
        width: fit-content;
        max-width: 78%;
        background-color: #EA580C;
        color: #FFFFFF;
        padding: 10px 18px;
        border-radius: 12px 12px 2px 12px;
        font-weight: 500;
        font-size: 0.93rem;
        line-height: 1.45;
        word-wrap: break-word;
        text-align: left;
    }

    /* Option Action Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #141414;
        color: #EDEDED;
        border: 1px solid #282828;
        border-radius: 8px;
        padding: 12px 18px;
        font-size: 0.94rem;
        font-weight: 500;
        text-align: left;
        transition: all 0.15s ease;
        margin-bottom: 8px;
    }
    div.stButton > button:hover {
        background-color: #1C1C1C;
        border-color: #EA580C;
        color: #FFFFFF;
    }
    div.stButton > button:active {
        background-color: #EA580C;
        border-color: #F97316;
        color: #FFFFFF;
    }

    /* Recommendation Cards */
    .rec-card {
        background-color: #141414;
        border: 1px solid #242424;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .rec-card:hover {
        border-color: #383838;
    }
    .rec-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .rec-rank-badge {
        display: inline-block;
        background-color: #1A1A1A;
        color: #A3A3A3;
        border: 1px solid #2E2E2E;
        font-weight: 600;
        font-size: 0.74rem;
        padding: 4px 10px;
        border-radius: 5px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .rec-score-pill {
        background-color: #231C13;
        color: #FB923C;
        border: 1px solid #4D3319;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 4px 12px;
        border-radius: 5px;
    }
    .rec-title {
        font-family: 'Lora', 'Merriweather', 'Georgia', serif;
        font-size: 1.42rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 10px;
        letter-spacing: -0.01em;
        line-height: 1.3;
    }
    .rec-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 14px;
    }
    .meta-chip {
        display: inline-block;
        background-color: #1A1A1A;
        border: 1px solid #2B2B2B;
        color: #A3A3A3;
        font-size: 0.78rem;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 5px;
    }
    .rec-desc {
        color: #A3A3A3;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    .rec-section-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: #78716C;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
        margin-top: 14px;
    }
    .reason-list {
        margin: 0;
        padding-left: 20px;
        color: #D4D4D4;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-bottom: 14px;
    }
    .badge-tag {
        display: inline-block;
        background-color: #1A1A1A;
        border: 1px solid #2E2E2E;
        color: #D4D4D4;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 5px;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-career {
        display: inline-block;
        background-color: #1E1712;
        border: 1px solid #3D2817;
        color: #FED7AA;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 5px;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    /* Eligibility Notice Card */
    .notice-card {
        background-color: #1A1113;
        border: 1px solid #5C1D24;
        border-radius: 10px;
        padding: 18px 22px;
        color: #FECACA;
        margin-bottom: 22px;
    }
    .notice-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #F87171;
        margin-bottom: 6px;
    }
    .notice-body {
        font-size: 0.9rem;
        line-height: 1.5;
        color: #FCA5A5;
        margin-bottom: 8px;
    }

    /* Executive Score Summary Banner */
    .primary-stream-banner {
        background-color: #1F150D;
        border: 1px solid #6B2D0C;
        color: #FED7AA;
        padding: 16px 20px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
        margin-bottom: 20px;
        font-family: 'Lora', 'Georgia', serif;
    }

    /* Score Breakdown Table */
    .breakdown-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        margin-bottom: 16px;
        border: 1px solid #242424;
        border-radius: 8px;
        overflow: hidden;
    }
    .breakdown-table th, .breakdown-table td {
        padding: 10px 14px;
        text-align: left;
        border-bottom: 1px solid #242424;
        font-size: 0.88rem;
    }
    .breakdown-table th {
        background-color: #0F0F0F;
        color: #737373;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.76rem;
    }
    .breakdown-table td {
        background-color: #141414;
        color: #EDEDED;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #0E0E0E !important;
        border-right: 1px solid #222222 !important;
    }

    /* What-If Explorer Styles */
    .whatif-container {
        margin-top: 36px;
        padding-top: 24px;
        border-top: 1px solid #222222;
    }
    .whatif-badge-active {
        display: inline-block;
        background-color: #24140A;
        color: #FB923C;
        border: 1px solid #EA580C;
        font-weight: 700;
        font-size: 0.74rem;
        padding: 4px 12px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .whatif-badge-clean {
        display: inline-block;
        background-color: #171717;
        color: #A3A3A3;
        border: 1px solid #2E2E2E;
        font-weight: 600;
        font-size: 0.74rem;
        padding: 4px 12px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .whatif-impact-card {
        background-color: #141414;
        border: 1px solid #38271A;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
    .whatif-impact-title {
        font-family: 'Lora', 'Georgia', serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #FB923C;
        margin-bottom: 12px;
    }
    .whatif-impact-list {
        margin: 0;
        padding-left: 20px;
        color: #D4D4D4;
        font-size: 0.91rem;
        line-height: 1.6;
    }
    .whatif-answer-card {
        background-color: #141414;
        border: 1px solid #242424;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        transition: all 0.15s ease;
    }
    .whatif-answer-card:hover {
        border-color: #383838;
    }
    .whatif-answer-card.modified {
        border-color: #EA580C;
        background-color: #1A130E;
    }
    .whatif-q-cat {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #FB923C;
        letter-spacing: 0.08em;
        margin-bottom: 3px;
    }
    .whatif-q-title {
        font-family: 'Lora', 'Georgia', serif;
        font-weight: 600;
        font-size: 1.02rem;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .whatif-q-prompt {
        font-size: 0.86rem;
        color: #A3A3A3;
        line-height: 1.45;
        margin-bottom: 10px;
    }
    .whatif-val-badge {
        display: inline-block;
        background-color: #1A1A1A;
        color: #EDEDED;
        border: 1px solid #2E2E2E;
        border-radius: 5px;
        padding: 4px 12px;
        font-size: 0.86rem;
        font-weight: 500;
    }
    .whatif-val-badge.modified {
        background-color: #2D1A0E;
        color: #FED7AA;
        border-color: #EA580C;
        font-weight: 600;
    }
    .side-col-header {
        background-color: #171717;
        border: 1px solid #282828;
        border-radius: 6px;
        padding: 10px 14px;
        font-weight: 600;
        font-size: 0.88rem;
        text-align: center;
        margin-bottom: 14px;
        color: #A3A3A3;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .side-col-header.sim {
        border-color: #EA580C;
        background-color: #201309;
        color: #FED7AA;
    }
    .diff-reason-add {
        color: #4ADE80 !important;
        font-weight: 500;
    }
    .diff-reason-rem {
        color: #737373 !important;
        text-decoration: line-through;
        opacity: 0.7;
    }
    .score-badge-pos {
        display: inline-block;
        background-color: #162419;
        color: #4ADE80;
        border: 1px solid #1E4627;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 2px 7px;
        border-radius: 4px;
        margin-left: 6px;
    }
    .score-badge-neg {
        display: inline-block;
        background-color: #281216;
        color: #F87171;
        border: 1px solid #5C1E26;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 2px 7px;
        border-radius: 4px;
        margin-left: 6px;
    }
    .whatif-edit-box {
        background-color: #111111;
        border: 1px solid #EA580C;
        border-radius: 8px;
        padding: 16px;
        margin-top: 10px;
    }

    /* Orange Progress Bar */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #EA580C !important;
    }
</style>
""", unsafe_allow_html=True)

# Smooth auto-scroll function and sidebar feature navigation
def trigger_auto_scroll():
    """Injects auto-scroll, sticky progress pin, and sidebar feature navigation."""
    components.html(
        """
        <script>
            function bindFeatureNavigation() {
                try {
                    const doc = window.parent.document;
                    
                    // Pin sticky progress bar container
                    const progEl = doc.getElementById('section-progress');
                    if (progEl) {
                        const parentContainer = progEl.closest('.stElementContainer') || progEl.parentElement;
                        if (parentContainer) {
                            parentContainer.style.position = 'sticky';
                            parentContainer.style.top = '2.85rem';
                            parentContainer.style.zIndex = '995';
                        }
                    }

                    // Bind all sidebar feature links
                    const navLinks = doc.querySelectorAll('a[data-section-target]');
                    navLinks.forEach(link => {
                        if (link.dataset.navBound === "true") return;
                        link.dataset.navBound = "true";
                        
                        link.addEventListener('click', function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            const targetId = this.getAttribute('data-section-target');
                            const targetEl = doc.getElementById(targetId);
                            
                            if (targetEl) {
                                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                                targetEl.classList.remove('section-highlight');
                                void targetEl.offsetWidth;
                                targetEl.classList.add('section-highlight');
                                setTimeout(() => targetEl.classList.remove('section-highlight'), 1800);
                            } else {
                                const fallbackEl = doc.getElementById('section-assessment') || doc.getElementById('section-progress');
                                if (fallbackEl) {
                                    fallbackEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                                }
                            }
                        });
                    });
                } catch (err) {
                    console.log("Nav Error:", err);
                }
            }

            function smoothScrollDown() {
                try {
                    const doc = window.parent.document;
                    const isComplete = doc.getElementById('section-whatif') !== null;
                    if (!isComplete) {
                        const appView = doc.querySelector('[data-testid="stAppViewContainer"]') || 
                                        doc.querySelector('section.main') || 
                                        doc.querySelector('.main') ||
                                        doc.documentElement;
                        if (appView) {
                            appView.scrollTo({
                                top: appView.scrollHeight + 3000,
                                behavior: 'smooth'
                            });
                        }
                        window.parent.scrollTo({
                            top: doc.body.scrollHeight + 3000,
                            behavior: 'smooth'
                        });
                        const anchor = doc.getElementById('scroll-bottom-anchor');
                        if (anchor) {
                            anchor.scrollIntoView({ behavior: 'smooth', block: 'end' });
                        }
                    }
                } catch (err) {
                    console.log("Scroll Error:", err);
                }
            }

            bindFeatureNavigation();
            setTimeout(bindFeatureNavigation, 60);
            setTimeout(bindFeatureNavigation, 180);
            setTimeout(bindFeatureNavigation, 360);
            setTimeout(bindFeatureNavigation, 800);

            smoothScrollDown();
            setTimeout(smoothScrollDown, 80);
            setTimeout(smoothScrollDown, 220);
        </script>
        """,
        height=0,
        width=0,
    )

# Initialize state
init_session_state()

# Session calculations for sidebar navigation
is_done = st.session_state.get("is_complete", False)
progress_val = calculate_progress_percentage()

# Sidebar Navigation & System Reference
with st.sidebar:
    st.markdown("### System Navigator")
    st.markdown("Deterministic Career Routing & Advisory System")
    st.markdown("---")
    
    st.markdown("""
    <div class="sidebar-section-title">Platform Features</div>
    <div class="sidebar-section-subtitle">Select any feature to navigate directly to its section.</div>
    """, unsafe_allow_html=True)
    
    # Feature 1: Progress Tracker
    feat_progress_html = f"""
    <a href="#section-progress" data-section-target="section-progress" class="sidebar-feature-card">
        <div class="sidebar-feature-header">
            <span class="sidebar-feature-title">Progress Tracker</span>
            <span class="sidebar-feature-tag">{progress_val}% Tracked</span>
        </div>
        <div class="sidebar-feature-desc">Sticky real-time tracker monitoring diagnostic progress</div>
        <div class="sidebar-feature-cta">Navigate to section &rarr;</div>
    </a>
    """
    
    # Feature 2: Diagnostic Assessment
    status_assessment = "Complete" if is_done else "In Progress"
    feat_assessment_html = f"""
    <a href="#section-assessment" data-section-target="section-assessment" class="sidebar-feature-card">
        <div class="sidebar-feature-header">
            <span class="sidebar-feature-title">Diagnostic Assessment</span>
            <span class="sidebar-feature-tag">{status_assessment}</span>
        </div>
        <div class="sidebar-feature-desc">Adaptive decision-tree inquiry evaluating student profile</div>
        <div class="sidebar-feature-cta">Navigate to section &rarr;</div>
    </a>
    """
    
    # Feature 3: Career Recommendations
    rec_target = "section-recommendations" if is_done else "section-assessment"
    rec_tag = "Available" if is_done else "Locked"
    rec_tag_class = "" if is_done else "tag-locked"
    feat_recs_html = f"""
    <a href="#{rec_target}" data-section-target="{rec_target}" class="sidebar-feature-card">
        <div class="sidebar-feature-header">
            <span class="sidebar-feature-title">Career Recommendations</span>
            <span class="sidebar-feature-tag {rec_tag_class}">{rec_tag}</span>
        </div>
        <div class="sidebar-feature-desc">Ranked stream and degree pathways with match scoring</div>
        <div class="sidebar-feature-cta">Navigate to section &rarr;</div>
    </a>
    """
    
    # Feature 4: Evaluation Rationale
    eval_target = "section-evaluation" if is_done else "section-assessment"
    eval_tag = "Available" if is_done else "Locked"
    eval_tag_class = "" if is_done else "tag-locked"
    feat_eval_html = f"""
    <a href="#{eval_target}" data-section-target="{eval_target}" class="sidebar-feature-card">
        <div class="sidebar-feature-header">
            <span class="sidebar-feature-title">Evaluation Rationale</span>
            <span class="sidebar-feature-tag {eval_tag_class}">{eval_tag}</span>
        </div>
        <div class="sidebar-feature-desc">Subject performance scores (0-10) and rule breakdown</div>
        <div class="sidebar-feature-cta">Navigate to section &rarr;</div>
    </a>
    """
    
    # Feature 5: Prerequisite Constraints
    prereq_target = "section-prerequisites" if is_done else "section-assessment"
    prereq_tag = "Available" if is_done else "Locked"
    prereq_tag_class = "" if is_done else "tag-locked"
    feat_prereq_html = f"""
    <a href="#{prereq_target}" data-section-target="{prereq_target}" class="sidebar-feature-card">
        <div class="sidebar-feature-header">
            <span class="sidebar-feature-title">Prerequisite Constraints</span>
            <span class="sidebar-feature-tag {prereq_tag_class}">{prereq_tag}</span>
        </div>
        <div class="sidebar-feature-desc">Stream eligibility filters and alternative pathways</div>
        <div class="sidebar-feature-cta">Navigate to section &rarr;</div>
    </a>
    """
    
    # Feature 6: What-If Explorer
    whatif_target = "section-whatif" if is_done else "section-assessment"
    whatif_tag = "Simulation Ready" if is_done else "Locked"
    whatif_tag_class = "" if is_done else "tag-locked"
    feat_whatif_html = f"""
    <a href="#{whatif_target}" data-section-target="{whatif_target}" class="sidebar-feature-card">
        <div class="sidebar-feature-header">
            <span class="sidebar-feature-title">What-If Explorer</span>
            <span class="sidebar-feature-tag {whatif_tag_class}">{whatif_tag}</span>
        </div>
        <div class="sidebar-feature-desc">Counterfactual simulator to test alternative choices</div>
        <div class="sidebar-feature-cta">Navigate to section &rarr;</div>
    </a>
    """
    
    st.markdown(f"""
    <div class="sidebar-features-container">
        {feat_progress_html}
        {feat_assessment_html}
        {feat_recs_html}
        {feat_eval_html}
        {feat_prereq_html}
        {feat_whatif_html}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Session")
    if st.button("Restart Assessment", key="sidebar_restart_btn"):
        restart_assessment()
        st.rerun()

    if is_done and st.session_state.get("what_if_answers"):
        if st.session_state.what_if_answers != st.session_state.answers:
            if st.button("Reset What-If Answers", key="sidebar_reset_whatif_btn"):
                reset_what_if()
                st.rerun()

    st.markdown("---")
    st.markdown("#### Core Rules")
    st.markdown("- **Deterministic Architecture**: Rule matrices and decision-tree logic without black-box ML.")
    st.markdown("- **Prerequisite Filters**: Enforces Class 12 stream constraints (e.g. Mathematics required for standard B.Tech).")
    st.markdown("- **Guided Progression**: Single active inquiry with instant option selection.")

    st.markdown("---")
    st.markdown("#### Evaluation Matrix")
    st.caption("Subject Scoring Formula (Marks x Interest):")
    st.code("> 75%:  VI:10 | I:9 | N:5 | NI:2\n50-75%: VI:9  | I:8 | N:4 | NI:2\n< 50%:  VI:6  | I:5 | N:2 | NI:0", language="text")

# Main Header
st.markdown("""
<div class="brand-header">
    <div class="brand-badge">Academic & Career Routing Engine</div>
    <div class="brand-title">Rule-Based Career Guidance</div>
    <div class="brand-subtitle">Adaptive Decision-Tree Advisory for Class 10 & Class 12 Students in India</div>
</div>
""", unsafe_allow_html=True)

# Sticky Progress Indicator
prog_status_text = "Assessment Complete" if is_done else "Assessment Progress"
st.markdown(f"""
<div class="sticky-progress-container" id="section-progress">
    <div class="sticky-progress-inner">
        <div class="sticky-progress-label-row">
            <div class="sticky-progress-title">
                <span class="sticky-progress-dot"></span>
                <span>{prog_status_text}</span>
            </div>
            <div class="sticky-progress-val">{progress_val}%</div>
        </div>
        <div class="sticky-progress-track">
            <div class="sticky-progress-fill" style="width: {progress_val}%;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Render Chat Stream
st.markdown('<div class="chat-wrapper" id="section-assessment">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["sender"] == "bot":
        st.markdown(f'<div class="bot-row"><div class="bot-bubble">{msg["text"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-row"><div class="user-bubble">{msg["text"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Active Question Options
if not st.session_state.is_complete and st.session_state.current_question:
    current_q = st.session_state.current_question
    options = current_q.get("options", [])
    
    if options:
        for idx, option in enumerate(options):
            if st.button(option, key=f"btn_{current_q.get('id', 'q')}_{idx}"):
                process_user_selection(option)
                st.rerun()

# Render Final Recommendations
if st.session_state.is_complete and st.session_state.recommendations:
    st.markdown('<div id="section-recommendations" class="section-anchor"></div>', unsafe_allow_html=True)
    st.markdown("### Recommendation Summary")
    
    rec_payload = st.session_state.recommendations
    
    # ---------------- Class 10 Recommendations ----------------
    if rec_payload["type"] == "class_10":
        streams = rec_payload["streams"]
        top_stream = streams[0]
        subject_scores = rec_payload.get("subject_scores", {})
        
        st.markdown(f"""
        <div class="primary-stream-banner">
            Primary Recommended Stream: {top_stream['name']} ({top_stream['match_score']}% Match)
        </div>
        """, unsafe_allow_html=True)
        
        # Subject Score Breakdown Table
        st.markdown('<div id="section-evaluation" class="section-anchor"></div>', unsafe_allow_html=True)
        if subject_scores:
            with st.expander("Detailed Subject Performance Scores (0-10)", expanded=False):
                subj_labels = {
                    "math_score": "Mathematics",
                    "physics_score": "Physics",
                    "chemistry_score": "Chemistry",
                    "biology_score": "Biology",
                    "social_score": "Social Studies",
                    "language_score": "Language & Literature"
                }
                rows_html = ""
                for k, label in subj_labels.items():
                    val = subject_scores.get(k, 0)
                    rows_html += f"<tr><td><strong>{label}</strong></td><td>{val} / 10</td></tr>"
                    
                st.markdown(f"""
                <table class="breakdown-table">
                    <thead><tr><th>Subject Area</th><th>Evaluated Score</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
                """, unsafe_allow_html=True)

        st.markdown('<div id="section-prerequisites" class="section-anchor"></div>', unsafe_allow_html=True)
        for idx, item in enumerate(streams):
            rank_label = f"Stream Option #{idx+1}"
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-top-row">
                    <span class="rec-rank-badge">{rank_label}</span>
                    <span class="rec-score-pill">{item['match_score']}% Match</span>
                </div>
                <div class="rec-title">{item['name']}</div>
                <div style="margin-bottom: 14px;">
                    <div class="rec-section-title">Evaluation Rationale</div>
                    <ul class="reason-list">
                        {''.join([f'<li>{r}</li>' for r in item['reasons']])}
                    </ul>
                </div>
                <div style="margin-bottom: 14px;">
                    <div class="rec-section-title">Future Degree Pathways</div>
                    {''.join([f'<span class="badge-tag">{d}</span>' for d in item['future_degrees']])}
                </div>
                <div>
                    <div class="rec-section-title">Target Career Roles</div>
                    {''.join([f'<span class="badge-career">{c}</span>' for c in item['future_careers']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- Class 12 Recommendations ----------------
    elif rec_payload["type"] == "class_12":
        rec_data = rec_payload["data"]
        top_recs = rec_data["top_recommendations"]
        ineligible_alerts = rec_data.get("ineligible_alerts", [])
        
        # Display Ineligible Prerequisites Notice
        st.markdown('<div id="section-prerequisites" class="section-anchor"></div>', unsafe_allow_html=True)
        if ineligible_alerts:
            for alert in ineligible_alerts:
                alts_str = ", ".join(alert.get("suggested_alternatives", []))
                st.markdown(f"""
                <div class="notice-card">
                    <div class="notice-title">Prerequisite Constraint Notice: {alert['name']}</div>
                    <div class="notice-body">{alert['reason']}</div>
                    <div style="font-size: 0.88rem; color: #FECACA;">
                        <strong>Suggested Eligible Alternatives:</strong> {alts_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div id="section-evaluation" class="section-anchor"></div>', unsafe_allow_html=True)
        for idx, rec in enumerate(top_recs):
            rank_label = f"Top Recommendation #{idx+1}"
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-top-row">
                    <span class="rec-rank-badge">{rank_label}</span>
                    <span class="rec-score-pill">{rec['match_score']}% Match</span>
                </div>
                <div class="rec-title">{rec['name']}</div>
                <div class="rec-meta-row">
                    <span class="meta-chip">{rec.get('category', 'Pathway')}</span>
                    <span class="meta-chip">Duration: {rec.get('degree_duration', '3-4 Years')}</span>
                    <span class="meta-chip">Industry Demand: {rec.get('industry_demand', 'High')}</span>
                </div>
                <div class="rec-desc">{rec['description']}</div>
                <div style="margin-bottom: 14px;">
                    <div class="rec-section-title">Evaluation Rationale</div>
                    <ul class="reason-list">
                        {''.join([f'<li>{r}</li>' for r in rec['reasons']])}
                    </ul>
                </div>
                <div style="margin-bottom: 14px;">
                    <div class="rec-section-title">Essential Skills</div>
                    {''.join([f'<span class="badge-tag">{s}</span>' for s in rec['top_skills']])}
                </div>
                <div>
                    <div class="rec-section-title">Target Career Roles</div>
                    {''.join([f'<span class="badge-career">{c}</span>' for c in rec['future_careers']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # =============================================================
    # WHAT-IF / COUNTERFACTUAL MODE EXPLORER
    # =============================================================
    st.markdown("""
    <div class="whatif-container" id="section-whatif">
        <div class="brand-badge">
            Counterfactual Lab
        </div>
        <h2 style="font-size: 1.65rem; font-weight: 600; color: #FFFFFF; margin-top: 4px; margin-bottom: 6px;">
            What-If Explorer
        </h2>
        <p style="color: #A3A3A3; font-size: 0.92rem; margin-bottom: 18px;">
            Simulate alternative academic and interest scenarios by modifying previous answers. The deterministic decision-tree
            and eligibility matrices will recalculate and show side-by-side impacts in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize what_if_answers if not yet present
    if st.session_state.what_if_answers is None:
        st.session_state.what_if_answers = dict(st.session_state.answers)

    # Catalog of editable answers
    catalog = get_editable_answers_catalog(st.session_state.what_if_answers)
    orig_catalog = get_editable_answers_catalog(st.session_state.answers)
    orig_catalog_map = {item["key"]: item for item in orig_catalog}

    is_what_if_modified = (st.session_state.what_if_answers != st.session_state.answers)

    # Action / Status Bar
    col_status, col_reset = st.columns([3, 1])
    with col_status:
        if is_what_if_modified:
            # Count modified answers
            mod_count = sum(
                1 for item in catalog
                if item["key"] in orig_catalog_map and orig_catalog_map[item["key"]]["current_raw"] != item["current_raw"]
            )
            st.markdown(
                f'<span class="whatif-badge-active">Simulation Active: {mod_count} Modified Answer{"s" if mod_count > 1 else ""}</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="whatif-badge-clean">Baseline Assessment (All Original Answers Active)</span>',
                unsafe_allow_html=True
            )
    with col_reset:
        if is_what_if_modified:
            if st.button("Reset What-If", key="reset_what_if_main_btn"):
                reset_what_if()
                st.rerun()

    # Display Informational Notices (e.g. branch switches, stream dependency updates)
    if st.session_state.what_if_notices:
        for notice in st.session_state.what_if_notices:
            st.info(notice)

    # Simulation Evaluation & Comparison
    if is_what_if_modified:
        what_if_rec = generate_what_if_recommendations(st.session_state.what_if_answers)
        comp = compute_what_if_comparison(
            st.session_state.recommendations,
            what_if_rec,
            st.session_state.answers,
            st.session_state.what_if_answers
        )

        # 1. Highlights & Impact Banner
        if comp.get("highlights"):
            highlights_html = "".join([f"<li>{h}</li>" for h in comp["highlights"]])
            st.markdown(f"""
            <div class="whatif-impact-card">
                <div class="whatif-impact-title">Simulation Impact Summary</div>
                <ul class="whatif-impact-list">
                    {highlights_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 2. Eligibility Constraint Alerts
        if comp.get("eligibility_changes"):
            for ec in comp["eligibility_changes"]:
                if ec["status_after"] == "Ineligible":
                    alts_str = ", ".join(ec.get("suggested_alternatives", []))
                    st.markdown(f"""
                    <div class="notice-card">
                        <div class="notice-title">Prerequisite Constraint Triggered: {ec['name']}</div>
                        <div class="notice-body">{ec['reason']}</div>
                        {f'<div style="font-size: 0.88rem; color: #FECACA;"><strong>Suggested Alternatives:</strong> {alts_str}</div>' if alts_str else ''}
                    </div>
                    """, unsafe_allow_html=True)
                elif ec["status_after"] == "Eligible":
                    st.success(f"{ec['name']} is now ELIGIBLE under this counterfactual scenario.")

        # 3. Side-by-Side Comparison Columns
        st.markdown("#### Side-by-Side Comparison")

        if comp.get("is_cross_level"):
            # Switched between Class 10 and Class 12
            col_b, col_s = st.columns(2)
            col_b.markdown('<div class="side-col-header">Original Baseline Assessment</div>', unsafe_allow_html=True)
            col_b.info(f"Original assessment was for {comp['orig_type'].replace('_', ' ').title()}.")
            col_s.markdown('<div class="side-col-header sim">What-If Simulation</div>', unsafe_allow_html=True)
            col_s.info(f"What-If simulation is for {comp['new_type'].replace('_', ' ').title()}.")
        elif comp.get("orig_type") == "class_12":
            # Class 12 comparison
            col_base, col_sim = st.columns(2)
            orig_top = comp.get("top_before", [])
            new_top = comp.get("top_after", [])
            orig_stream = rec_payload.get("stream", "Class 12")
            new_stream = what_if_rec.get("stream", "Class 12")

            col_base.markdown(f'<div class="side-col-header">Original Baseline ({orig_stream})</div>', unsafe_allow_html=True)
            for idx, r in enumerate(orig_top):
                col_base.markdown(f"""
                <div class="rec-card" style="padding: 20px; margin-bottom: 14px;">
                    <div class="rec-top-row">
                        <span class="rec-rank-badge">Rank #{idx+1}</span>
                        <span class="rec-score-pill">{r['match_score']}% Match</span>
                    </div>
                    <div class="rec-title" style="font-size: 1.2rem;">{r['name']}</div>
                    <div style="font-size: 0.8rem; color: #A3A3A3; margin-bottom: 10px;">
                        {r.get('category', 'Pathway')} • {r.get('degree_duration', '3-4 Years')}
                    </div>
                    <div class="rec-section-title" style="font-size: 0.74rem;">Evaluation Rationale</div>
                    <ul class="reason-list" style="font-size: 0.88rem; margin-bottom: 0;">
                        {''.join([f'<li>{reason}</li>' for reason in r['reasons']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            col_sim.markdown(f'<div class="side-col-header sim">What-If Simulation ({new_stream})</div>', unsafe_allow_html=True)
            for idx, r in enumerate(new_top):
                pdiff = next((p for p in comp.get("pathway_diffs", []) if p["id"] == r["id"]), None)
                score_delta_badge = ""
                rank_shift_note = ""
                if pdiff and pdiff["score_delta"] is not None:
                    delta = pdiff["score_delta"]
                    if delta > 0:
                        score_delta_badge = f'<span class="score-badge-pos">+{delta}%</span>'
                    elif delta < 0:
                        score_delta_badge = f'<span class="score-badge-neg">{delta}%</span>'

                if pdiff and pdiff["rank_before"] and pdiff["rank_before"] != (idx + 1):
                    rank_shift_note = f' <span style="font-size: 0.74rem; color: #FB923C;">(was #{pdiff["rank_before"]})</span>'
                elif pdiff and not pdiff["rank_before"]:
                    rank_shift_note = ' <span style="font-size: 0.74rem; color: #4ADE80;">(New Entry)</span>'

                reasons_html = ""
                added_set = set(pdiff["added_reasons"]) if pdiff else set()
                for reason in r["reasons"]:
                    if reason in added_set:
                        reasons_html += f'<li><span class="diff-reason-add">+ {reason}</span></li>'
                    else:
                        reasons_html += f'<li>{reason}</li>'

                col_sim.markdown(f"""
                <div class="rec-card" style="padding: 20px; margin-bottom: 14px; border-color: #EA580C;">
                    <div class="rec-top-row">
                        <span class="rec-rank-badge" style="background-color: #1F140D; color: #FB923C; border-color: #5C280C;">Rank #{idx+1}{rank_shift_note}</span>
                        <div>
                            <span class="rec-score-pill">{r['match_score']}% Match</span>
                            {score_delta_badge}
                        </div>
                    </div>
                    <div class="rec-title" style="font-size: 1.2rem; color: #FFFFFF;">{r['name']}</div>
                    <div style="font-size: 0.8rem; color: #A3A3A3; margin-bottom: 10px;">
                        {r.get('category', 'Pathway')} • {r.get('degree_duration', '3-4 Years')}
                    </div>
                    <div class="rec-section-title" style="font-size: 0.74rem;">Evaluation Rationale (+ Highlights)</div>
                    <ul class="reason-list" style="font-size: 0.88rem; margin-bottom: 0;">
                        {reasons_html}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Class 10 comparison
            col_base, col_sim = st.columns(2)
            orig_streams = rec_payload.get("streams", [])
            new_streams = what_if_rec.get("streams", [])

            col_base.markdown('<div class="side-col-header">Original Baseline Streams</div>', unsafe_allow_html=True)
            for idx, s in enumerate(orig_streams[:3]):
                col_base.markdown(f"""
                <div class="rec-card" style="padding: 20px; margin-bottom: 14px;">
                    <div class="rec-top-row">
                        <span class="rec-rank-badge">Option #{idx+1}</span>
                        <span class="rec-score-pill">{s['match_score']}% Match</span>
                    </div>
                    <div class="rec-title" style="font-size: 1.2rem;">{s['name']}</div>
                    <ul class="reason-list" style="font-size: 0.88rem; margin-bottom: 0;">
                        {''.join([f'<li>{r}</li>' for r in s['reasons']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            col_sim.markdown('<div class="side-col-header sim">What-If Simulation Streams</div>', unsafe_allow_html=True)
            for idx, s in enumerate(new_streams[:3]):
                sdiff = next((sd for sd in comp.get("stream_diffs", []) if sd["stream_id"] == s["stream_id"]), None)
                score_delta_badge = ""
                rank_shift_note = ""
                if sdiff and sdiff["score_delta"] != 0:
                    delta = sdiff["score_delta"]
                    if delta > 0:
                        score_delta_badge = f'<span class="score-badge-pos">+{delta}%</span>'
                    else:
                        score_delta_badge = f'<span class="score-badge-neg">{delta}%</span>'
                if sdiff and sdiff["rank_before"] and sdiff["rank_before"] != (idx + 1):
                    rank_shift_note = f' <span style="font-size: 0.74rem; color: #FB923C;">(was #{sdiff["rank_before"]})</span>'

                reasons_html = ""
                added_set = set(sdiff["added_reasons"]) if sdiff else set()
                for reason in s["reasons"]:
                    if reason in added_set:
                        reasons_html += f'<li><span class="diff-reason-add">+ {reason}</span></li>'
                    else:
                        reasons_html += f'<li>{reason}</li>'

                col_sim.markdown(f"""
                <div class="rec-card" style="padding: 20px; margin-bottom: 14px; border-color: #EA580C;">
                    <div class="rec-top-row">
                        <span class="rec-rank-badge" style="background-color: #1F140D; color: #FB923C; border-color: #5C280C;">Option #{idx+1}{rank_shift_note}</span>
                        <div>
                            <span class="rec-score-pill">{s['match_score']}% Match</span>
                            {score_delta_badge}
                        </div>
                    </div>
                    <div class="rec-title" style="font-size: 1.2rem; color: #FFFFFF;">{s['name']}</div>
                    <ul class="reason-list" style="font-size: 0.88rem; margin-bottom: 0;">
                        {reasons_html}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # Subject Performance Comparison Table
            if comp.get("subject_diffs"):
                with st.expander("Subject Performance Score Shifts (0-10)", expanded=True):
                    rows = ""
                    for sd in comp["subject_diffs"]:
                        d = sd["score_delta"]
                        d_str = f"+{d}" if d > 0 else (str(d) if d < 0 else "0")
                        d_style = 'color: #4ADE80; font-weight: 700;' if d > 0 else ('color: #F87171; font-weight: 700;' if d < 0 else 'color: #737373;')
                        rows += f"<tr><td><strong>{sd['subject']}</strong></td><td>{sd['score_before']} / 10</td><td>{sd['score_after']} / 10</td><td style='{d_style}'>{d_str}</td></tr>"
                    st.markdown(f"""
                    <table class="breakdown-table">
                        <thead><tr><th>Subject Area</th><th>Baseline Score</th><th>What-If Score</th><th>Shift</th></tr></thead>
                        <tbody>{rows}</tbody>
                    </table>
                    """, unsafe_allow_html=True)

    # 4. Answers Summary & Interactive Editor
    st.markdown("---")
    st.markdown("#### Assessment Answers (Interactive Controls)")
    st.caption("Review all answered questions below. Select Edit on any question to change your choice and simulate real-time impacts.")

    for item in catalog:
        orig_item = orig_catalog_map.get(item["key"], item)
        is_item_mod = (orig_item["current_raw"] != item["current_raw"])
        card_class = "whatif-answer-card modified" if is_item_mod else "whatif-answer-card"
        badge_class = "whatif-val-badge modified" if is_item_mod else "whatif-val-badge"

        if is_item_mod:
            val_display_html = f'<span style="text-decoration: line-through; color: #737373; margin-right: 8px;">{orig_item["current_display"]}</span> ➔ <strong style="color: #FB923C;">{item["current_display"]}</strong>'
        else:
            val_display_html = f'<span>{item["current_display"]}</span>'

        c_card, c_act = st.columns([4, 1])
        with c_card:
            st.markdown(f"""
            <div class="{card_class}">
                <div class="whatif-q-cat">{item['category']}</div>
                <div class="whatif-q-title">{item['title']}</div>
                <div class="whatif-q-prompt">{item['prompt']}</div>
                <div class="{badge_class}">{val_display_html}</div>
            </div>
            """, unsafe_allow_html=True)
        with c_act:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Edit", key=f"edit_btn_{item['key']}"):
                st.session_state.what_if_editing_key = item["key"]
                st.rerun()

        # Active inline editor if this question is being edited
        if st.session_state.what_if_editing_key == item["key"]:
            with st.container():
                st.markdown(f"""
                <div class="whatif-edit-box">
                    <div style="font-weight: 700; color: #FB923C; margin-bottom: 6px;">Editing: {item['title']}</div>
                    <div style="font-size: 0.88rem; color: #A3A3A3; margin-bottom: 12px;">{item['prompt']}</div>
                </div>
                """, unsafe_allow_html=True)

                cur_opt = item["current_display"]
                opt_idx = item["options"].index(cur_opt) if cur_opt in item["options"] else 0
                selected_new_val = st.selectbox(
                    f"Choose new option for {item['title']}:",
                    options=item["options"],
                    index=opt_idx,
                    key=f"whatif_sel_{item['key']}"
                )

                col_save, col_cancel = st.columns(2)
                if col_save.button("Apply & Recalculate", key=f"save_btn_{item['key']}", type="primary"):
                    updated, notices = apply_what_if_update(
                        st.session_state.what_if_answers,
                        item["key"],
                        selected_new_val
                    )
                    st.session_state.what_if_answers = updated
                    st.session_state.what_if_notices = notices
                    st.session_state.what_if_editing_key = None
                    st.rerun()
                if col_cancel.button("Cancel", key=f"cancel_btn_{item['key']}"):
                    st.session_state.what_if_editing_key = None
                    st.rerun()

    st.markdown("---")
    if st.button("Start New Guidance Session", key="results_restart_btn"):
        restart_assessment()
        st.rerun()

# Bottom anchor & auto-scroll
st.markdown('<div id="scroll-bottom-anchor"></div>', unsafe_allow_html=True)
trigger_auto_scroll()


