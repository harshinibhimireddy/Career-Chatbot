"""
Recommendation Engine for Class 12 Career Guidance.
Applies strict eligibility filters, rule-based match scoring, candidate ranking,
and formats the Top 3 career recommendations with detailed explanations.
"""

from data.careers import CAREERS_DB
from engine.eligibility import check_pathway_eligibility

# Mapping streams to candidate pathway IDs
STREAM_PATHWAY_MAP = {
    "MPC": [
        "btech_cse", "btech_aiml", "btech_ece", "btech_eee", 
        "btech_mech", "btech_civil", "bba_management", 
        "business_analytics", "integrated_law", "chartered_accountancy",
        "pharmacy", "bioinformatics"
    ],
    "BiPC": [
        "mbbs_medicine", "bds_dental", "pharmacy", "biotechnology", 
        "biomedical_science", "allied_health", "bioinformatics",
        "psychology", "bba_management", "integrated_law",
        "btech_cse"  # Included to test eligibility filtering!
    ],
    "PCMB": [
        "btech_cse", "btech_aiml", "mbbs_medicine", "biotechnology", 
        "biomedical_science", "bioinformatics", "btech_ece", "bds_dental", 
        "business_analytics", "integrated_law", "pharmacy"
    ],
    "Commerce": [
        "bcom_finance", "bba_management", "chartered_accountancy", 
        "business_analytics", "integrated_law", "journalism_communication", 
        "psychology", "public_policy_civil_services"
    ],
    "Humanities": [
        "psychology", "integrated_law", "journalism_communication", 
        "public_policy_civil_services", "bba_management", "bcom_finance"
    ]
}


def score_pathway_for_user(pathway_id: str, stream: str, answers: dict) -> tuple[int, list]:
    """
    Rule-based scoring function for a given pathway based on user answers.
    Returns: (match_score: int [0-100], reasons: list[str])
    """
    pathway_info = CAREERS_DB.get(pathway_id, {})
    base_score = 65
    reasons = []

    domain_choice = answers.get("c12_domain_choice", "")
    deep_dive = answers.get("c12_deep_dive", "")
    marks_level = answers.get("c12_marks_level", "")
    interest_level = answers.get("c12_interest_level", "")
    has_math_comm = answers.get("comm_has_math", "")
    pcmb_pref = answers.get("pcmb_pref", "")

    # 1. Marks Rule
    if marks_level == "Above 75%":
        base_score += 12
        reasons.append("High academic performance (>75%) in core Class 12 subjects")
    elif marks_level == "50% to 75%":
        base_score += 7
        reasons.append("Consistent academic standing (50%-75%) in Class 12")
    else:
        base_score += 2
        reasons.append("Fulfills academic baseline requirements for university admissions")

    # 2. Interest Level Rule
    if interest_level == "Very Interested":
        base_score += 10
        reasons.append("Expressed very high passion in the primary subject domain")
    elif interest_level == "Interested":
        base_score += 6
        reasons.append("Positive aptitude and interest in subject fundamentals")

    # 3. Stream-Specific Aptitude Checks
    if stream in ["MPC", "PCMB"]:
        reasons.append(f"Satisfies mandatory Class 12 science prerequisite ({stream})")
    elif stream == "Commerce":
        if has_math_comm == "Yes, Commerce with Math":
            if pathway_id in ["business_analytics", "chartered_accountancy", "bcom_finance"]:
                base_score += 6
                reasons.append("Commerce with Mathematics background strengthens analytical and quantitative modeling capabilities")
    elif stream == "Humanities":
        reasons.append("Strong humanities foundation in societal analysis, communication, and legal concepts")

    # 4. PCMB Preference Rule
    if stream == "PCMB":
        if "Tech Focus" in pcmb_pref and pathway_id in ["btech_cse", "btech_aiml", "btech_ece"]:
            base_score += 8
            reasons.append("Chosen preference aligns strongly with technology & engineering")
        elif "Clinical Focus" in pcmb_pref and pathway_id in ["mbbs_medicine", "bds_dental"]:
            base_score += 8
            reasons.append("Chosen preference aligns with clinical medical practice")
        elif "Bio-Tech Focus" in pcmb_pref and pathway_id in ["biomedical_science", "biotechnology", "bioinformatics"]:
            base_score += 10
            reasons.append("Direct passion for dual-science intersection of biology and technology")

    # 5. Domain Alignment Rules (Class 12)
    # Engineering
    if pathway_id == "btech_cse":
        if "Programming" in domain_choice or "Software" in domain_choice:
            base_score += 15
            reasons.append("Strong alignment with programming, algorithmic problem-solving, and software development")
        if "Cloud" in deep_dive or "software" in deep_dive.lower():
            base_score += 6
            reasons.append("Career preference targets high-scale cloud platforms and enterprise applications")
    elif pathway_id == "btech_aiml":
        if "Artificial Intelligence" in domain_choice or "Data Science" in domain_choice:
            base_score += 16
            reasons.append("High enthusiasm for Machine Learning, Artificial Intelligence, and Big Data Engineering")
        if "Deep Learning" in deep_dive or "Neural Networks" in deep_dive:
            base_score += 6
            reasons.append("Targeting deep learning models, neural networks, and autonomous AI systems")
    elif pathway_id == "btech_ece":
        if "Electronics" in domain_choice or "Microchips" in domain_choice:
            base_score += 15
            reasons.append("High aptitude for semiconductor hardware, circuit design, and wireless communications")
        if "VLSI" in deep_dive or "Chip" in deep_dive:
            base_score += 6
            reasons.append("Targeting VLSI chip design and embedded IoT architecture")
    elif pathway_id == "btech_eee":
        if "Electrical" in domain_choice or "Power" in domain_choice:
            base_score += 15
            reasons.append("Strong interest in power systems, electric mobility (EVs), and renewable energy")
        if "Electric Vehicles" in deep_dive or "Power Grid" in deep_dive:
            base_score += 6
            reasons.append("Direct alignment with EV powertrain systems and smart energy grid automation")
    elif pathway_id == "btech_mech":
        if "Machines" in domain_choice or "Automotive" in domain_choice or "Robotics" in domain_choice:
            base_score += 15
            reasons.append("Passion for mechanical design, robotics, thermodynamics, and manufacturing")
        if "Robotics" in deep_dive or "CAD" in deep_dive:
            base_score += 6
            reasons.append("Career focus on CAD design, robotics automation, and aerospace systems")
    elif pathway_id == "btech_civil":
        if "Civil" in domain_choice or "Structures" in domain_choice or "Infrastructure" in domain_choice:
            base_score += 15
            reasons.append("Strong interest in structural planning, sustainable infrastructure, and smart cities")
        if "Urban Planning" in deep_dive or "Highway" in deep_dive:
            base_score += 6
            reasons.append("Aspiration to lead large-scale national infrastructure and urban engineering projects")

    # Medical & Life Sciences
    elif pathway_id in ["mbbs_medicine", "bds_dental"]:
        if "Patient Care" in domain_choice or "Clinical Diagnosis" in domain_choice or "MBBS" in domain_choice:
            base_score += 16
            reasons.append("Deep commitment to direct patient care, clinical diagnosis, and healing diseases")
        if "hospitals" in deep_dive.lower() or "clinical practices" in deep_dive.lower() or "doctor" in deep_dive.lower():
            base_score += 6
            reasons.append("Aspiration to practice medicine in acute clinical and hospital environments")
    elif pathway_id == "pharmacy":
        if "Medicines" in domain_choice or "Pharmacology" in domain_choice or "B.Pharm" in domain_choice:
            base_score += 15
            reasons.append("Enthusiasm for drug discovery, medicinal chemistry, and pharmaceutical manufacturing")
        if "Pharmaceutical" in deep_dive or "drug trials" in deep_dive:
            base_score += 6
            reasons.append("Targeting pharmaceutical R&D labs and clinical drug trials")
    elif pathway_id == "biotechnology":
        if "Biotechnology" in domain_choice or "Genetics" in domain_choice or "B.Sc Biotech" in domain_choice:
            base_score += 15
            reasons.append("Strong curiosity for recombinant DNA, genetics, and biotechnology innovations")
        if "Genetic engineering" in deep_dive or "vaccine" in deep_dive:
            base_score += 6
            reasons.append("Focus on CRISPR gene editing, vaccine formulations, and bioprocess technology")
    elif pathway_id == "biomedical_science":
        if "Technology" in domain_choice or "Bio-Devices" in domain_choice or "Biomedical" in domain_choice:
            base_score += 15
            reasons.append("Passion for bridging life sciences with healthcare technology and diagnostics")
        if "diagnostic tools" in deep_dive or "health apps" in deep_dive or "prosthetics" in deep_dive:
            base_score += 6
            reasons.append("Targeting medical diagnostic instrumentation, bio-sensors, and healthcare informatics")
    elif pathway_id == "allied_health":
        if "Allied" in domain_choice or "Nursing" in domain_choice or "Hospital" in domain_choice:
            base_score += 15
            reasons.append("Dedication to vital patient support, physical therapy, radiology, and healthcare delivery")
        if "therapy" in deep_dive.lower() or "radiology" in deep_dive.lower():
            base_score += 6
            reasons.append("Direct engagement in clinical therapy, patient rehabilitation, and diagnostic imaging")
    elif pathway_id == "bioinformatics":
        if "Bioinformatics" in domain_choice or "Computational Biology" in domain_choice or "Data" in domain_choice:
            base_score += 16
            reasons.append("Strong interest in computational genomics, biological big data, and protein modeling")
        if "genomic datasets" in deep_dive or "biological big data" in deep_dive:
            base_score += 6
            reasons.append("Focused on high-throughput genomic data pipelines and computational biology")

    # Commerce & Management
    elif pathway_id in ["bcom_finance", "chartered_accountancy"]:
        if "Auditing" in domain_choice or "Accounting" in domain_choice or "CA" in domain_choice or "Taxation" in domain_choice:
            base_score += 15
            reasons.append("Strong aptitude for financial accounting, corporate taxation, and statutory auditing")
        if "balance sheets" in deep_dive or "forensic accounting" in deep_dive or "tax strategy" in deep_dive:
            base_score += 6
            reasons.append("Goal to become a premier Chartered Accountant (CA) or corporate tax advisor")
    elif pathway_id == "bba_management":
        if "Management" in domain_choice or "Leadership" in domain_choice or "BBA" in domain_choice:
            base_score += 15
            reasons.append("Demonstrated interest in corporate leadership, brand marketing, and operations management")
        if "Leading product teams" in deep_dive or "startup" in deep_dive:
            base_score += 6
            reasons.append("Focus on executive management, business development, and enterprise leadership")
    elif pathway_id == "business_analytics":
        if "Analytics" in domain_choice or "FinTech" in domain_choice or "Intelligence" in domain_choice:
            base_score += 16
            reasons.append("High alignment with quantitative business analytics, PowerBI dashboards, and FinTech")
        if "Visualizing business data" in deep_dive or "SQL" in deep_dive:
            base_score += 6
            reasons.append("Aspiration to drive corporate strategy through SQL data pipelines and business intelligence")

    # Law & Humanities
    elif pathway_id == "integrated_law":
        if "Law" in domain_choice or "Legal" in domain_choice or "Justice" in domain_choice:
            base_score += 15
            reasons.append("Strong interest in legal advocacy, corporate law, constitutional justice, and litigation")
        if "courts" in deep_dive.lower() or "contracts" in deep_dive.lower() or "justice" in deep_dive.lower():
            base_score += 6
            reasons.append("Goal to excel in corporate legal consulting or courtroom litigation")
    elif pathway_id == "psychology":
        if "Psychology" in domain_choice or "Mental Health" in domain_choice or "Counseling" in domain_choice:
            base_score += 16
            reasons.append("Deep empathy and fascination with human cognition, behavioral science, and clinical therapy")
        if "mental health" in deep_dive.lower() or "therapy" in deep_dive.lower() or "individuals" in deep_dive.lower():
            base_score += 6
            reasons.append("Dedicated to psychometric counseling, mental healthcare, and behavioral analysis")
    elif pathway_id == "journalism_communication":
        if "Journalism" in domain_choice or "Media" in domain_choice or "Communication" in domain_choice:
            base_score += 15
            reasons.append("Strong verbal articulation, creative storytelling, and passion for digital media and public relations")
        if "investigative" in deep_dive.lower() or "documentary" in deep_dive.lower() or "media strategy" in deep_dive.lower():
            base_score += 6
            reasons.append("Aspiration to lead investigative journalism and multi-channel digital media strategy")
    elif pathway_id == "public_policy_civil_services":
        if "Civil Services" in domain_choice or "Governance" in domain_choice or "UPSC" in domain_choice or "Policy" in domain_choice:
            base_score += 15
            reasons.append("Commitment to public governance, national socio-economic policy, and UPSC Civil Services (IAS/IPS)")
        if "national policies" in deep_dive.lower() or "administration" in deep_dive.lower() or "foreign affairs" in deep_dive.lower():
            base_score += 6
            reasons.append("Aiming for leadership in district administration, diplomacy, and public policy think-tanks")

    final_score = min(98, max(50, base_score))
    return final_score, list(dict.fromkeys(reasons))


def generate_class_12_recommendations(stream: str, answers: dict) -> dict:
    """
    Generates structured career recommendations for Class 12 student.
    
    Returns:
    {
        "top_recommendations": [ list of top 3 dicts ],
        "ineligible_alerts": [ list of prerequisite gap dicts if user selected ineligible domain ]
    }
    """
    candidate_ids = STREAM_PATHWAY_MAP.get(stream, [])
    eligible_recommendations = []
    ineligible_alerts = []

    domain_choice = answers.get("c12_domain_choice", "")

    for pid in candidate_ids:
        pathway_info = CAREERS_DB.get(pid)
        if not pathway_info:
            continue

        # Check eligibility first
        elig_result = check_pathway_eligibility(pid, stream, answers)

        if elig_result["eligible"]:
            score, reasons = score_pathway_for_user(pid, stream, answers)
            rec_card = {
                "id": pid,
                "name": pathway_info["name"],
                "match_score": score,
                "eligibility": "Eligible",
                "category": pathway_info.get("category", "Degree Pathway"),
                "description": pathway_info.get("description", ""),
                "reasons": reasons,
                "future_careers": pathway_info.get("future_careers", []),
                "top_skills": pathway_info.get("top_skills", []),
                "industry_demand": pathway_info.get("industry_demand", "High"),
                "degree_duration": pathway_info.get("degree_duration", "3-4 Years")
            }
            eligible_recommendations.append(rec_card)
        else:
            # If user actively expressed interest in this domain (e.g. BiPC selecting B.Tech CSE)
            if pid == "btech_cse" and ("Programming" in domain_choice or "Software" in domain_choice):
                ineligible_alerts.append({
                    "name": pathway_info["name"],
                    "eligibility": "Ineligible",
                    "reason": elig_result["reason"],
                    "suggested_alternatives": elig_result.get("suggested_alternatives", [])
                })

    # Sort eligible pathways descending by match score
    eligible_recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    top_3 = eligible_recommendations[:3]

    return {
        "top_recommendations": top_3,
        "ineligible_alerts": ineligible_alerts
    }
