"""
Eligibility constraints database for Class 12 Indian Academic Streams.
Defines required Class 12 subjects, allowed/disqualified streams, and alternative pathway recommendations.
"""

ELIGIBILITY_CONSTRAINTS = {
    # -------------------------------------------------------------
    # Engineering & Technology Pathways (Require Class 12 Mathematics)
    # -------------------------------------------------------------
    "btech_cse": {
        "required_subjects": ["math"],
        "allowed_streams": ["MPC", "PCMB"],
        "disqualified_streams": ["BiPC", "Commerce", "Humanities"],
        "explanation": "Standard B.Tech Computer Science & Engineering strictly requires Class 12 Mathematics as a mandatory prerequisite by AICTE/UGC regulations.",
        "suggested_alternatives": [
            "Biomedical Science & Health Informatics",
            "B.Sc / B.Tech Biotechnology",
            "Bioinformatics & Computational Biology",
            "BCA (where universities admit life science students without 12th math)"
        ]
    },
    "btech_aiml": {
        "required_subjects": ["math"],
        "allowed_streams": ["MPC", "PCMB"],
        "disqualified_streams": ["BiPC", "Commerce", "Humanities"],
        "explanation": "B.Tech Artificial Intelligence & Data Science requires foundational calculus, discrete math, and linear algebra in Class 12.",
        "suggested_alternatives": [
            "Bioinformatics & Computational Biology",
            "Biomedical Science & Health Informatics",
            "BBA / B.Sc Business Analytics & FinTech"
        ]
    },
    "btech_ece": {
        "required_subjects": ["math", "physics"],
        "allowed_streams": ["MPC", "PCMB"],
        "disqualified_streams": ["BiPC", "Commerce", "Humanities"],
        "explanation": "B.Tech Electronics & Communication requires Class 12 Mathematics and Physics for circuit analysis and semiconductor physics.",
        "suggested_alternatives": [
            "Biomedical Science & Health Informatics",
            "B.Sc Biotechnology"
        ]
    },
    "btech_eee": {
        "required_subjects": ["math", "physics"],
        "allowed_streams": ["MPC", "PCMB"],
        "disqualified_streams": ["BiPC", "Commerce", "Humanities"],
        "explanation": "B.Tech Electrical & Electronics Engineering requires Class 12 Mathematics and Physics for power electromagnetics and systems.",
        "suggested_alternatives": [
            "Biomedical Science & Health Informatics"
        ]
    },
    "btech_mech": {
        "required_subjects": ["math", "physics"],
        "allowed_streams": ["MPC", "PCMB"],
        "disqualified_streams": ["BiPC", "Commerce", "Humanities"],
        "explanation": "B.Tech Mechanical Engineering requires Class 12 Mathematics and Mechanics in Physics.",
        "suggested_alternatives": [
            "Biomedical Science & Health Informatics",
            "B.Sc Biotechnology"
        ]
    },
    "btech_civil": {
        "required_subjects": ["math", "physics"],
        "allowed_streams": ["MPC", "PCMB"],
        "disqualified_streams": ["BiPC", "Commerce", "Humanities"],
        "explanation": "B.Tech Civil Engineering requires Class 12 Mathematics and Physics for statics and structural mechanics.",
        "suggested_alternatives": [
            "Public Policy & Civil Services (UPSC)",
            "5-Year Integrated Law (BA LLB / BBA LLB)"
        ]
    },

    # -------------------------------------------------------------
    # Clinical & Medical Healthcare Pathways (Require Class 12 Biology)
    # -------------------------------------------------------------
    "mbbs_medicine": {
        "required_subjects": ["biology", "chemistry", "physics"],
        "allowed_streams": ["BiPC", "PCMB"],
        "disqualified_streams": ["MPC", "Commerce", "Humanities"],
        "explanation": "MBBS / Clinical Medicine requires Class 12 Biology, Physics, and Chemistry (PCB) and qualifying the NEET-UG examination.",
        "suggested_alternatives": [
            "B.Tech Biomedical Engineering",
            "Bioinformatics & Computational Biology",
            "B.Pharmacy / Pharm.D"
        ]
    },
    "bds_dental": {
        "required_subjects": ["biology", "chemistry", "physics"],
        "allowed_streams": ["BiPC", "PCMB"],
        "disqualified_streams": ["MPC", "Commerce", "Humanities"],
        "explanation": "BDS (Dental Surgery) requires Class 12 Biology, Physics, and Chemistry and NEET-UG qualification.",
        "suggested_alternatives": [
            "Biomedical Science & Health Informatics",
            "B.Pharmacy / Pharm.D"
        ]
    },
    "pharmacy": {
        "required_subjects": ["chemistry", "biology_or_math"],
        "allowed_streams": ["BiPC", "PCMB", "MPC"],
        "disqualified_streams": ["Commerce", "Humanities"],
        "explanation": "B.Pharmacy / Pharm.D admits students with Physics, Chemistry, and either Biology or Mathematics.",
        "suggested_alternatives": [
            "B.Com Accounting & Corporate Finance",
            "5-Year Integrated Law (BA LLB / BBA LLB)"
        ]
    },
    "biotechnology": {
        "required_subjects": ["biology_or_math", "chemistry"],
        "allowed_streams": ["BiPC", "PCMB", "MPC"],
        "disqualified_streams": ["Commerce", "Humanities"],
        "explanation": "Biotechnology requires foundational science background in Biology or Mathematics with Chemistry.",
        "suggested_alternatives": [
            "BBA / B.Sc Business Analytics & FinTech",
            "BA / B.Sc Psychology & Behavioral Sciences"
        ]
    },
    "biomedical_science": {
        "required_subjects": ["biology", "chemistry"],
        "allowed_streams": ["BiPC", "PCMB"],
        "disqualified_streams": ["MPC", "Commerce", "Humanities"],
        "explanation": "Biomedical Science & Health Informatics requires Class 12 Biology and Chemistry background.",
        "suggested_alternatives": [
            "B.Tech Electronics & Communication",
            "B.Tech Computer Science & Engineering"
        ]
    },
    "allied_health": {
        "required_subjects": ["biology"],
        "allowed_streams": ["BiPC", "PCMB"],
        "disqualified_streams": ["MPC", "Commerce", "Humanities"],
        "explanation": "Allied Health Sciences (Nursing, Physiotherapy BPT, Radiology Tech) require Class 12 Biology.",
        "suggested_alternatives": [
            "BA / B.Sc Psychology & Behavioral Sciences",
            "5-Year Integrated Law"
        ]
    },
    "bioinformatics": {
        "required_subjects": ["biology_or_math"],
        "allowed_streams": ["PCMB", "BiPC", "MPC"],
        "disqualified_streams": ["Commerce", "Humanities"],
        "explanation": "Bioinformatics & Computational Biology is open to science students with Bio and/or Math.",
        "suggested_alternatives": [
            "BBA / B.Sc Business Analytics & FinTech"
        ]
    },

    # -------------------------------------------------------------
    # Commerce, Management, Law & Humanities (Open to various streams)
    # -------------------------------------------------------------
    "bcom_finance": {
        "required_subjects": [],
        "allowed_streams": ["Commerce", "MPC", "PCMB", "Humanities"],
        "disqualified_streams": [],
        "explanation": "B.Com / Corporate Finance is open to Commerce students as well as Science and Humanities graduates.",
        "suggested_alternatives": []
    },
    "bba_management": {
        "required_subjects": [],
        "allowed_streams": ["Commerce", "MPC", "BiPC", "PCMB", "Humanities"],
        "disqualified_streams": [],
        "explanation": "BBA / Management is universally open to students from any Class 12 academic stream.",
        "suggested_alternatives": []
    },
    "chartered_accountancy": {
        "required_subjects": [],
        "allowed_streams": ["Commerce", "MPC", "PCMB", "Humanities", "BiPC"],
        "disqualified_streams": [],
        "explanation": "Chartered Accountancy (CA / CS / CMA) Foundation is open to students from all 12th streams.",
        "suggested_alternatives": []
    },
    "business_analytics": {
        "required_subjects": [],
        "allowed_streams": ["Commerce", "MPC", "PCMB", "BiPC", "Humanities"],
        "disqualified_streams": [],
        "explanation": "Business Analytics & FinTech welcomes students from analytical, commerce, or science backgrounds.",
        "suggested_alternatives": []
    },
    "integrated_law": {
        "required_subjects": [],
        "allowed_streams": ["Humanities", "Commerce", "MPC", "BiPC", "PCMB"],
        "disqualified_streams": [],
        "explanation": "5-Year Integrated Law (BA LLB / BBA LLB) is open to all streams via national entrance exams (CLAT, AILET, SLAT).",
        "suggested_alternatives": []
    },
    "psychology": {
        "required_subjects": [],
        "allowed_streams": ["Humanities", "BiPC", "Commerce", "MPC", "PCMB"],
        "disqualified_streams": [],
        "explanation": "BA / B.Sc Psychology is open to all streams, with strong alignment for Humanities and Life Science students.",
        "suggested_alternatives": []
    },
    "journalism_communication": {
        "required_subjects": [],
        "allowed_streams": ["Humanities", "Commerce", "MPC", "BiPC", "PCMB"],
        "disqualified_streams": [],
        "explanation": "BA Journalism, Media & Mass Communication is open to students from any Class 12 academic stream.",
        "suggested_alternatives": []
    },
    "public_policy_civil_services": {
        "required_subjects": [],
        "allowed_streams": ["Humanities", "Commerce", "MPC", "BiPC", "PCMB"],
        "disqualified_streams": [],
        "explanation": "Social Sciences, Public Policy, and UPSC Civil Services preparation are open to all Class 12 backgrounds.",
        "suggested_alternatives": []
    }
}
