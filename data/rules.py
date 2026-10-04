"""
Rules database and decision tree routing logic for Class 10 and Class 12 guidance.
Determines adaptive question branching, stream recommendations, and pathway match scoring.
"""

from engine.scoring import compute_all_subject_scores

# -------------------------------------------------------------
# CLASS 10 DECISION TREE ROUTING & SCORING
# -------------------------------------------------------------

def evaluate_class_10_branch(answers: dict) -> str:
    """
    Determines the adaptive question branch for Class 10 based on calculated subject scores.
    Returns branch key: 'pcmb_dual', 'mpc_tech', 'bipc_health', 'social_lang', or 'commerce_general'.
    """
    scores = compute_all_subject_scores(answers)
    
    m_score = scores.get("math_score", 0)
    p_score = scores.get("physics_score", 0)
    c_score = scores.get("chemistry_score", 0)
    b_score = scores.get("biology_score", 0)
    s_score = scores.get("social_score", 0)
    l_score = scores.get("language_score", 0)

    # 1. Check PCMB (All science and math are strong: >= 8 out of 10)
    if m_score >= 8 and p_score >= 8 and b_score >= 8 and c_score >= 8:
        return "pcmb_dual"
        
    # 2. Check Math & Physics strong
    if (m_score + p_score) >= 16 and (m_score + p_score) >= (b_score + c_score):
        return "mpc_tech"
        
    # 3. Check Biology & Chemistry strong
    if (b_score + c_score) >= 16 and (b_score + c_score) > (m_score + p_score):
        return "bipc_health"
        
    # 4. Check Social & Language strong
    if (s_score + l_score) >= 15 and (s_score + l_score) > (m_score + p_score) and (s_score + l_score) > (b_score + c_score):
        return "social_lang"
        
    # 5. Relative strength evaluation
    tech_score = m_score + p_score + c_score
    bio_score = b_score + c_score + p_score
    arts_score = s_score + l_score
    comm_score = s_score + m_score + l_score
    
    if bio_score > tech_score and bio_score > arts_score and b_score >= 5:
        return "bipc_health"
    elif tech_score >= arts_score and tech_score >= comm_score:
        return "mpc_tech"
    elif arts_score >= comm_score and arts_score >= 12:
        return "social_lang"
    else:
        return "commerce_general"


def score_class_10_streams(answers: dict) -> list:
    """
    Calculates match percentage and recommendations for all Class 11 Streams.
    Returns ranked list of stream recommendations with match score, explanation, future careers.
    """
    scores = compute_all_subject_scores(answers)
    
    m_score = scores.get("math_score", 0)
    p_score = scores.get("physics_score", 0)
    c_score = scores.get("chemistry_score", 0)
    b_score = scores.get("biology_score", 0)
    s_score = scores.get("social_score", 0)
    l_score = scores.get("language_score", 0)
    
    primary_adaptive = answers.get("c10_adaptive_primary", "")
    followup_adaptive = answers.get("c10_adaptive_followup", "")

    # MPC Score Calculation
    mpc_base = (m_score * 0.45) + (p_score * 0.35) + (c_score * 0.20)
    mpc_match = int(mpc_base * 10)
    if primary_adaptive in [
        "Programming and software", "AI and robotics", "Electronics and hardware",
        "Machines and mechanical systems", "Buildings and infrastructure",
        "Scientific research", "Engineering and technology"
    ]:
        mpc_match = min(98, mpc_match + 8)
    if followup_adaptive in [
        "Software & High-Tech Industry", "Robotics & Automotive Engineering",
        "Semiconductor & Electronics Design", "Infrastructure & Construction Projects",
        "Pure Scientific Research & Space Tech", "I lean slightly more towards Engineering & AI"
    ]:
        mpc_match = min(98, mpc_match + 4)

    # BiPC Score Calculation
    bipc_base = (b_score * 0.45) + (c_score * 0.35) + (p_score * 0.20)
    bipc_match = int(bipc_base * 10)
    if primary_adaptive in [
        "Understanding the human body", "Diagnosing and treating patients",
        "Medicines and pharmaceuticals", "Genetics and biotechnology",
        "Healthcare technology", "Medicine and healthcare"
    ]:
        bipc_match = min(98, bipc_match + 8)
    if followup_adaptive in [
        "Hospitals & Direct Patient Care", "Pharmaceutical & Drug Formulation Labs",
        "Biotechnology & Genetics Research Institutes", "Medical Technology & Diagnostic Centers",
        "I lean slightly more towards Clinical Medicine"
    ]:
        bipc_match = min(98, bipc_match + 4)

    # PCMB Score Calculation
    pcmb_base = (m_score * 0.25) + (b_score * 0.25) + (p_score * 0.25) + (c_score * 0.25)
    pcmb_match = int(pcmb_base * 10)
    if primary_adaptive in ["Combining biology and technology", "I want to keep both options open"]:
        pcmb_match = min(96, pcmb_match + 10)
    if followup_adaptive in [
        "Yes, I love the intersection of Bio and Tech",
        "I prefer keeping options open for both NEET and JEE"
    ]:
        pcmb_match = min(96, pcmb_match + 6)

    # Commerce CEC Score Calculation
    cec_base = (s_score * 0.40) + (m_score * 0.30) + (l_score * 0.30)
    cec_match = int(cec_base * 10)
    if primary_adaptive in [
        "Financial markets & accounting", "Managing business operations & leadership",
        "Economics & trade analysis", "Economics and business", "Entrepreneurship & startups"
    ]:
        cec_match = min(95, cec_match + 8)
    if followup_adaptive in [
        "Becoming a Chartered Accountant (CA) or Financial Analyst",
        "Leading corporate companies as a Business Manager (BBA/MBA)",
        "Building a high-growth startup / Entrepreneurship",
        "Stock Market Trading, Wealth Management & Investment Banking"
    ]:
        cec_match = min(95, cec_match + 4)

    # Humanities HEC Score Calculation
    hec_base = (s_score * 0.50) + (l_score * 0.50)
    hec_match = int(hec_base * 10)
    if primary_adaptive in [
        "Society and people", "Government and public policy", "Writing and storytelling",
        "Communication and media", "Law and justice", "Psychology and human mind"
    ]:
        hec_match = min(95, hec_match + 8)
    if followup_adaptive in [
        "Legal Practice & Corporate Law (CLAT / LLB)",
        "Civil Services & Public Administration (UPSC / IAS)",
        "Clinical Psychology & Behavioral Science",
        "Media, Journalism & Creative Content Creation",
        "Economics, Policy Research & International Affairs"
    ]:
        hec_match = min(95, hec_match + 4)

    # Build explanations & results
    results = [
        {
            "stream_id": "MPC",
            "name": "MPC (Mathematics, Physics, Chemistry)",
            "match_score": mpc_match,
            "reasons": [
                f"Mathematics score: {m_score}/10, Physics score: {p_score}/10, Chemistry score: {c_score}/10",
                f"Core interest alignment: {primary_adaptive or 'Analytical Science & Technology'}",
                f"Preferred career focus: {followup_adaptive or 'Engineering Innovation'}"
            ],
            "future_degrees": [
                "B.Tech / B.E. (Computer Science, AI, ECE, Mechanical, Civil)",
                "B.Sc Computer Science / Data Science",
                "B.Arch (Architecture)",
                "NDA Defense Tech Wings"
            ],
            "future_careers": [
                "Software Engineer", "AI/ML Developer", "Electronics Engineer",
                "Data Scientist", "Architect", "Robotics Specialist"
            ]
        },
        {
            "stream_id": "BiPC",
            "name": "BiPC (Biology, Physics, Chemistry)",
            "match_score": bipc_match,
            "reasons": [
                f"Biology score: {b_score}/10, Chemistry score: {c_score}/10, Physics score: {p_score}/10",
                f"Core interest alignment: {primary_adaptive or 'Life Sciences & Healthcare'}",
                f"Preferred environment: {followup_adaptive or 'Clinical Care & Research Labs'}"
            ],
            "future_degrees": [
                "MBBS (Clinical Medicine)",
                "BDS (Dental Surgery)",
                "B.Pharmacy / Pharm.D",
                "B.Sc Biotechnology / Genetics",
                "B.Sc Nursing / Physiotherapy (BPT)"
            ],
            "future_careers": [
                "Medical Doctor / Physician", "Dentist", "Pharmacologist",
                "Biotechnologist", "Clinical Researcher", "Surgeon"
            ]
        },
        {
            "stream_id": "PCMB",
            "name": "PCMB (Physics, Chemistry, Mathematics, Biology)",
            "match_score": pcmb_match,
            "reasons": [
                f"Dual strength in Math ({m_score}/10) & Biology ({b_score}/10)",
                "Preserves both Engineering (JEE) and Medical (NEET) eligibility simultaneously",
                "Ideal for Interdisciplinary Bio-Engineering and Bioinformatics fields"
            ],
            "future_degrees": [
                "B.Tech Biomedical Engineering",
                "B.Tech / B.Sc Bioinformatics",
                "MBBS Medicine / BDS Dental",
                "B.Tech Biotechnology & Genetic Engineering"
            ],
            "future_careers": [
                "Biomedical Engineer", "Bioinformatics Scientist",
                "Medical Doctor", "Geneticist", "Bio-Data Scientist"
            ]
        },
        {
            "stream_id": "Commerce_CEC",
            "name": "Commerce / CEC (Civics, Economics, Commerce)",
            "match_score": cec_match,
            "reasons": [
                f"Social Studies score: {s_score}/10, Math score: {m_score}/10, Language score: {l_score}/10",
                f"Aptitude alignment: {primary_adaptive or 'Finance & Trade Management'}",
                f"Career horizon: {followup_adaptive or 'Corporate Accounting & Business'}"
            ],
            "future_degrees": [
                "B.Com (Honours) Accounting & Finance",
                "BBA (Bachelor of Business Administration)",
                "Chartered Accountancy (CA / CS Foundation)",
                "B.Sc Economics & Business Analytics"
            ],
            "future_careers": [
                "Chartered Accountant (CA)", "Financial Analyst",
                "Investment Banker", "Corporate Manager", "Business Consultant"
            ]
        },
        {
            "stream_id": "Humanities_HEC",
            "name": "Humanities / HEC (History, Economics, Civics / Arts)",
            "match_score": hec_match,
            "reasons": [
                f"Social Studies score: {s_score}/10, Language & Literature score: {l_score}/10",
                f"Aptitude alignment: {primary_adaptive or 'Societal Governance, Law & Psychology'}",
                f"Career goal: {followup_adaptive or 'Public Leadership & Legal Advocacy'}"
            ],
            "future_degrees": [
                "5-Year Integrated BA LLB / BBA LLB (Law)",
                "BA / B.Sc Psychology & Behavioral Sciences",
                "BA Journalism & Mass Communication",
                "BA Political Science & UPSC Foundation"
            ],
            "future_careers": [
                "Corporate Lawyer / Advocate", "Psychologist / Counselor",
                "Digital Journalist / Media Strategist", "Civil Servant (IAS/IPS)"
            ]
        }
    ]

    # Sort descending by match score
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
