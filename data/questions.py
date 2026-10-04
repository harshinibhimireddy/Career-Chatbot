"""
Question database for the Career Guidance Chatbot.
Contains all structured questions, options, keys, and dynamic option definitions
for Class 10 and Class 12 adaptive decision trees.
"""

# Master Question 1
MASTER_QUESTION = {
    "id": "q_master_entry",
    "question": "Welcome to Career Guidance India! When do you need career guidance?",
    "options": [
        "After Class 10",
        "After Class 12"
    ],
    "type": "single_choice"
}

# -------------------------------------------------------------
# CLASS 10 QUESTIONS
# -------------------------------------------------------------

# Subject evaluation questions for Class 10
CLASS_10_SUBJECT_QUESTIONS = [
    {
        "subject_id": "math",
        "name": "Mathematics",
        "marks_q_id": "q_c10_math_marks",
        "marks_question": "How was your academic performance in Mathematics in Class 10?",
        "interest_q_id": "q_c10_math_interest",
        "interest_question": "How interested are you in Mathematics and numerical problem-solving?",
    },
    {
        "subject_id": "physics",
        "name": "Physics",
        "marks_q_id": "q_c10_physics_marks",
        "marks_question": "How was your academic performance in Physics / Physical Science?",
        "interest_q_id": "q_c10_physics_interest",
        "interest_question": "How interested are you in Physics (mechanics, electricity, optics, scientific laws)?",
    },
    {
        "subject_id": "chemistry",
        "name": "Chemistry",
        "marks_q_id": "q_c10_chemistry_marks",
        "marks_question": "How was your academic performance in Chemistry?",
        "interest_q_id": "q_c10_chemistry_interest",
        "interest_question": "How interested are you in Chemistry (reactions, elements, compounds, lab experiments)?",
    },
    {
        "subject_id": "biology",
        "name": "Biology",
        "marks_q_id": "q_c10_biology_marks",
        "marks_question": "How was your academic performance in Biology / Life Science?",
        "interest_q_id": "q_c10_biology_interest",
        "interest_question": "How interested are you in Biology (living organisms, human physiology, plants, genetics)?",
    },
    {
        "subject_id": "social",
        "name": "Social Studies",
        "marks_q_id": "q_c10_social_marks",
        "marks_question": "How was your academic performance in Social Studies (History, Geography, Civics, Economics)?",
        "interest_q_id": "q_c10_social_interest",
        "interest_question": "How interested are you in Social Studies (society, governance, history, economic systems)?",
    },
    {
        "subject_id": "language",
        "name": "Language",
        "marks_q_id": "q_c10_language_marks",
        "marks_question": "How was your academic performance in Language & Literature (English / Regional)?",
        "interest_q_id": "q_c10_language_interest",
        "interest_question": "How interested are you in Language, Literature, creative writing, and communication?",
    }
]

MARKS_OPTIONS = [
    {"label": "Above 75%", "value": "above_75"},
    {"label": "50% to 75%", "value": "50_75"},
    {"label": "Below 50%", "value": "below_50"}
]

INTEREST_OPTIONS = [
    {"label": "Very Interested", "value": "very_interested"},
    {"label": "Interested", "value": "interested"},
    {"label": "Neutral", "value": "neutral"},
    {"label": "Not Interested", "value": "not_interested"}
]

# Adaptive questions for Class 10 based on scoring profile
CLASS_10_ADAPTIVE_QUESTIONS = {
    # 1. When Mathematics & Physics are strong
    "mpc_tech": {
        "primary": {
            "id": "q_c10_mpc_interest",
            "question": "You show strong aptitude in Mathematics and Physics! What interests you most in technology and engineering?",
            "options": [
                "Programming and software",
                "AI and robotics",
                "Electronics and hardware",
                "Machines and mechanical systems",
                "Buildings and infrastructure",
                "Scientific research"
            ]
        },
        "follow_up": {
            "id": "q_c10_mpc_followup",
            "question": "What type of career setting excites you most?",
            "options": [
                "Software & High-Tech Industry",
                "Robotics & Automotive Engineering",
                "Semiconductor & Electronics Design",
                "Infrastructure & Construction Projects",
                "Pure Scientific Research & Space Tech"
            ]
        }
    },
    # 2. When Biology & Chemistry are strong
    "bipc_health": {
        "primary": {
            "id": "q_c10_bipc_interest",
            "question": "You show high aptitude in Biology and Chemistry! What interests you most in life sciences and healthcare?",
            "options": [
                "Understanding the human body",
                "Diagnosing and treating patients",
                "Medicines and pharmaceuticals",
                "Laboratory experiments",
                "Genetics and biotechnology",
                "Healthcare technology"
            ]
        },
        "follow_up": {
            "id": "q_c10_bipc_followup",
            "question": "Which work environment appeals to you most?",
            "options": [
                "Hospitals & Direct Patient Care",
                "Pharmaceutical & Drug Formulation Labs",
                "Biotechnology & Genetics Research Institutes",
                "Medical Technology & Diagnostic Centers"
            ]
        }
    },
    # 3. When Math, Physics, Biology, and Chemistry are all strong
    "pcmb_dual": {
        "primary": {
            "id": "q_c10_pcmb_interest",
            "question": "You have strengths across both Science and Mathematics! Which direction interests you most?",
            "options": [
                "Medicine and healthcare",
                "Engineering and technology",
                "Combining biology and technology",
                "I want to keep both options open"
            ]
        },
        "follow_up": {
            "id": "q_c10_pcmb_followup",
            "question": "Would you prefer specialized dual-science fields like Biomedical Engineering and Bioinformatics?",
            "options": [
                "Yes, I love the intersection of Bio and Tech",
                "I prefer keeping options open for both NEET and JEE",
                "I lean slightly more towards Engineering & AI",
                "I lean slightly more towards Clinical Medicine"
            ]
        }
    },
    # 4. When Social Studies and Language are strong
    "social_lang": {
        "primary": {
            "id": "q_c10_social_interest",
            "question": "You have strong aptitude in Social Studies and Language! Which field of human study excites you most?",
            "options": [
                "Society and people",
                "Government and public policy",
                "Economics and business",
                "Writing and storytelling",
                "Communication and media",
                "Law and justice",
                "Psychology and human mind"
            ]
        },
        "follow_up": {
            "id": "q_c10_social_followup",
            "question": "What is your primary career aspiration in the humanities domain?",
            "options": [
                "Legal Practice & Corporate Law (CLAT / LLB)",
                "Civil Services & Public Administration (UPSC / IAS)",
                "Clinical Psychology & Behavioral Science",
                "Media, Journalism & Creative Content Creation",
                "Economics, Policy Research & International Affairs"
            ]
        }
    },
    # 5. Commerce / Business focus
    "commerce_general": {
        "primary": {
            "id": "q_c10_commerce_interest",
            "question": "Which commercial or business focus appeals to you?",
            "options": [
                "Managing business operations & leadership",
                "Financial markets & accounting",
                "Economics & trade analysis",
                "Entrepreneurship & startups"
            ]
        },
        "follow_up": {
            "id": "q_c10_commerce_followup",
            "question": "What is your long-term goal in the business world?",
            "options": [
                "Becoming a Chartered Accountant (CA) or Financial Analyst",
                "Leading corporate companies as a Business Manager (BBA/MBA)",
                "Building a high-growth startup / Entrepreneurship",
                "Stock Market Trading, Wealth Management & Investment Banking"
            ]
        }
    }
}

# -------------------------------------------------------------
# CLASS 12 QUESTIONS
# -------------------------------------------------------------

CLASS_12_STREAM_QUESTION = {
    "id": "q_c12_stream",
    "question": "Which stream did you complete in Class 11 and Class 12?",
    "options": [
        "MPC",
        "BiPC",
        "PCMB",
        "Commerce",
        "Humanities"
    ]
}

# Stream specific deep decision-tree question sets for Class 12
CLASS_12_STREAM_QUESTIONS = {
    # ---------------- MPC ----------------
    "MPC": [
        {
            "id": "q_c12_mpc_marks",
            "question": "What was your approximate score range in Mathematics & Physics in Class 12?",
            "options": ["Above 75%", "50% to 75%", "Below 50%"],
            "key": "c12_marks_level"
        },
        {
            "id": "q_c12_mpc_math_interest",
            "question": "How would you rate your problem-solving and coding/analytical interest?",
            "options": ["Very Interested", "Interested", "Neutral", "Not Interested"],
            "key": "c12_interest_level"
        },
        {
            "id": "q_c12_mpc_domain",
            "question": "What domain in engineering and technology excites you most?",
            "options": [
                "Programming & Software Engineering",
                "Artificial Intelligence & Data Science",
                "Electronics, Microchips & Communication",
                "Electrical Power, Energy & EV Systems",
                "Machines, Automotive & Robotics",
                "Civil Structures, Smart Cities & Infrastructure",
                "Business Analytics & Quantitative Tech Management"
            ],
            "key": "c12_domain_choice"
        },
        {
            "id": "q_c12_mpc_deep_dive",
            "question": "What specific area of innovation would you like to build your career in?",
            "options": [
                "Cloud platforms, Web/Mobile apps & Enterprise software",
                "Deep Learning, Neural Networks & Autonomous Systems",
                "VLSI Chip design, Embedded Systems & IoT devices",
                "Electric Vehicles, Renewable Energy & Power Grid Automation",
                "Robotics, CAD Design & Drone Aerospace Systems",
                "Structural Architecture, Highway Networks & Urban Planning",
                "FinTech, Tech Consulting & Product Management"
            ],
            "key": "c12_deep_dive"
        }
    ],

    # ---------------- BiPC ----------------
    "BiPC": [
        {
            "id": "q_c12_bipc_marks",
            "question": "What was your score range in Biology & Chemistry in Class 12?",
            "options": ["Above 75%", "50% to 75%", "Below 50%"],
            "key": "c12_marks_level"
        },
        {
            "id": "q_c12_bipc_bio_interest",
            "question": "How would you rate your passion for Biological and Medical Sciences?",
            "options": ["Very Interested", "Interested", "Neutral", "Not Interested"],
            "key": "c12_interest_level"
        },
        {
            "id": "q_c12_bipc_domain",
            "question": "What life science or healthcare direction appeals to you most?",
            "options": [
                "Direct Patient Care & Clinical Diagnosis (MBBS / BDS)",
                "Medicines, Pharmacology & Drug Formulation (B.Pharm)",
                "Laboratory Research, Genetics & Biotechnology (B.Sc Biotech)",
                "Patient Care & Hospital Allied Services (Nursing / BPT)",
                "Combining Healthcare with Technology & Bio-Devices (Biomedical Science)",
                "Programming & Software Engineering (B.Tech CSE)"  # Intentionally triggers eligibility constraint rule!
            ],
            "key": "c12_domain_choice"
        },
        {
            "id": "q_c12_bipc_deep_dive",
            "question": "What is your primary professional setting preference?",
            "options": [
                "Treating patients directly in hospitals and clinical practices",
                "Pharmaceutical R&D labs and clinical drug trials",
                "Genetic engineering, vaccine research and biotech industries",
                "Hospital physical therapy, radiology and critical care delivery",
                "Medical instrumentation, health apps and biomedical diagnostic tools",
                "I am eager to explore software and computers"
            ],
            "key": "c12_deep_dive"
        }
    ],

    # ---------------- PCMB ----------------
    "PCMB": [
        {
            "id": "q_c12_pcmb_pref",
            "question": "You studied both Biology and Mathematics in Class 12! Which primary path do you lean towards?",
            "options": [
                "Engineering and Technology (Tech Focus)",
                "Medicine and Healthcare (Clinical Focus)",
                "Combining Biology and Technology (Bio-Tech Focus)",
                "Research, Data Science & Bioinformatics",
                "Both equally / Explore all top opportunities"
            ],
            "key": "pcmb_pref"
        },
        {
            "id": "q_c12_pcmb_marks",
            "question": "What was your score range across your Class 12 science subjects?",
            "options": ["Above 75%", "50% to 75%", "Below 50%"],
            "key": "c12_marks_level"
        },
        {
            "id": "q_c12_pcmb_domain",
            "question": "What domain interests you most?",
            "options": [
                "Artificial Intelligence & Software Engineering",
                "Biomedical Engineering & Medical Instrumentation",
                "Clinical Medicine (MBBS) & Surgery",
                "Biotechnology & Genetic Engineering",
                "Bioinformatics, Healthcare Analytics & Computational Biology"
            ],
            "key": "c12_domain_choice"
        },
        {
            "id": "q_c12_pcmb_deep_dive",
            "question": "What career horizon excites you most?",
            "options": [
                "Building AI models and high-scale software systems",
                "Designing artificial organs, prosthetics & medical robotic devices",
                "Practicing as a specialized medical doctor or surgeon",
                "Developing novel therapeutics, vaccines and CRISPR gene therapies",
                "Analyzing massive genomic datasets and biological big data"
            ],
            "key": "c12_deep_dive"
        }
    ],

    # ---------------- Commerce ----------------
    "Commerce": [
        {
            "id": "q_c12_comm_math",
            "question": "Did you study Mathematics in Class 12 alongside Commerce?",
            "options": ["Yes, Commerce with Math", "No, Commerce without Math"],
            "key": "comm_has_math"
        },
        {
            "id": "q_c12_comm_marks",
            "question": "What was your score range in Accountancy & Economics in Class 12?",
            "options": ["Above 75%", "50% to 75%", "Below 50%"],
            "key": "c12_marks_level"
        },
        {
            "id": "q_c12_comm_interest",
            "question": "How would you rate your interest in business numbers, finance, and commerce?",
            "options": ["Very Interested", "Interested", "Neutral", "Not Interested"],
            "key": "c12_interest_level"
        },
        {
            "id": "q_c12_comm_domain",
            "question": "Which commercial or business career path interests you most?",
            "options": [
                "Corporate Auditing, Accounting & Taxation (CA / CS / CMA)",
                "Banking, Corporate Finance & Investment Management",
                "Business Management, Leadership & Marketing (BBA)",
                "Data Analytics, FinTech & Business Intelligence",
                "Corporate Law & Legal Advisory (B.Com LLB / BBA LLB)"
            ],
            "key": "c12_domain_choice"
        },
        {
            "id": "q_c12_comm_deep_dive",
            "question": "What specific role in business appeals to you?",
            "options": [
                "Auditing balance sheets, forensic accounting and tax strategy",
                "Managing investment portfolios, equities and venture capital",
                "Leading product teams, operations, marketing and startup ventures",
                "Visualizing business data with SQL, PowerBI and Python",
                "Handling corporate contracts, intellectual property and mergers"
            ],
            "key": "c12_deep_dive"
        }
    ],

    # ---------------- Humanities ----------------
    "Humanities": [
        {
            "id": "q_c12_hum_marks",
            "question": "What was your score range in Social Sciences / English in Class 12?",
            "options": ["Above 75%", "50% to 75%", "Below 50%"],
            "key": "c12_marks_level"
        },
        {
            "id": "q_c12_hum_interest",
            "question": "How interested are you in human society, behavior, governance, and communication?",
            "options": ["Very Interested", "Interested", "Neutral", "Not Interested"],
            "key": "c12_interest_level"
        },
        {
            "id": "q_c12_hum_domain",
            "question": "Which field of human studies or public domain excites you most?",
            "options": [
                "Human Psychology, Mental Health & Counseling",
                "Legal Studies, Constitutional Law & Justice (BA LLB)",
                "Journalism, Digital Media, PR & Communication",
                "Civil Services, Governance & Public Policy (UPSC)",
                "Economics, International Relations & Diplomacy",
                "Literature, Creative Writing & Digital Arts"
            ],
            "key": "c12_domain_choice"
        },
        {
            "id": "q_c12_hum_deep_dive",
            "question": "What impact do you want your future career to have?",
            "options": [
                "Helping individuals with mental health, therapy & organizational behavior",
                "Advocating for justice in courts, legal advisory & corporate law",
                "Investigative journalism, documentary production & media strategy",
                "Formulating national policies, public governance & district administration",
                "Economic policy research, foreign affairs & international NGOs",
                "Publishing books, creative media content & academic teaching"
            ],
            "key": "c12_deep_dive"
        }
    ]
}
