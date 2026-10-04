"""
Master database of streams, degrees, pathways, and associated career options.
Contains real-life Indian education pathways, descriptions, skills, industry demand, and job roles.
"""

CAREERS_DB = {
    # -------------------------------------------------------------
    # CLASS 10 STREAM RECOMMENDATIONS
    # -------------------------------------------------------------
    "MPC": {
        "id": "MPC",
        "name": "MPC (Mathematics, Physics, Chemistry)",
        "type": "class_10_stream",
        "description": "Ideal for students with strong analytical skills, mathematical aptitude, and interest in technology, engineering, physical sciences, architecture, or defense tech.",
        "future_degrees": [
            "B.Tech / B.E. (Computer Science, AI, ECE, Mechanical, Civil)",
            "B.Sc Computer Science / Data Science / Physics",
            "B.Arch (Architecture)",
            "National Defence Academy (NDA - Technical Wings)",
            "B.Tech Aerospace / Robotics / Semiconductor Tech"
        ],
        "future_careers": [
            "Software Development Engineer",
            "AI / Machine Learning Engineer",
            "VLSI / Chip Design Engineer",
            "Data Scientist",
            "Robotics & Automation Specialist",
            "Aerospace Engineer",
            "Architect / Urban Planner"
        ],
        "stream_focus": "Core Physical Sciences, Quantitative Analysis & Mathematics"
    },
    "BiPC": {
        "id": "BiPC",
        "name": "BiPC (Biology, Physics, Chemistry)",
        "type": "class_10_stream",
        "description": "Designed for students passionate about biological systems, human physiology, medicine, clinical healthcare, drug research, genetics, or environmental sciences.",
        "future_degrees": [
            "MBBS (Bachelor of Medicine, Bachelor of Surgery)",
            "BDS (Bachelor of Dental Surgery)",
            "B.Pharmacy / Pharm.D (Doctor of Pharmacy)",
            "B.Sc Biotechnology / Genetics / Microbiology",
            "B.Sc Nursing / Physiotherapy (BPT)",
            "B.Sc Biomedical Science / Medical Laboratory Tech"
        ],
        "future_careers": [
            "Medical Doctor / Surgeon",
            "Dentist / Orthodontist",
            "Clinical Pharmacologist / Drug Researcher",
            "Biotechnologist / Geneticist",
            "Biomedical Scientist",
            "Physiotherapist / Healthcare Specialist"
        ],
        "stream_focus": "Life Sciences, Human Physiology & Clinical Medicine"
    },
    "PCMB": {
        "id": "PCMB",
        "name": "PCMB (Physics, Chemistry, Mathematics, Biology)",
        "type": "class_10_stream",
        "description": "Comprehensive dual-science stream keeping both Engineering (JEE) and Medical (NEET) pathways open, ideal for bio-engineering, bioinformatics, and interdisciplinary innovation.",
        "future_degrees": [
            "B.Tech Biomedical Engineering / Medical Devices",
            "B.Tech / B.Sc Bioinformatics & Computational Biology",
            "MBBS / BDS / Medical Clinical Programs",
            "B.Tech Biotechnology & Genetic Engineering",
            "B.Sc Biostatistics & Healthcare Data Analytics"
        ],
        "future_careers": [
            "Biomedical Engineer",
            "Bioinformatics Scientist",
            "Medical Doctor / Physician",
            "Geneticist & CRISPR Researcher",
            "Health-Tech Product Developer",
            "Biostatistician / Data Scientist"
        ],
        "stream_focus": "Integrated Sciences, Bio-Engineering & Computational Biology"
    },
    "Commerce_CEC": {
        "id": "Commerce_CEC",
        "name": "Commerce / CEC (Civics, Economics, Commerce)",
        "type": "class_10_stream",
        "description": "Suited for students interested in finance, trade, corporate operations, accounting, economic policy, stock markets, and entrepreneurship.",
        "future_degrees": [
            "B.Com (Honours) in Accounting & Finance",
            "BBA (Bachelor of Business Administration)",
            "Chartered Accountancy (CA / CS / CMA Foundation)",
            "B.Sc Economics / Econometrics",
            "BBA in Business Analytics & FinTech"
        ],
        "future_careers": [
            "Chartered Accountant (CA)",
            "Investment Banker & Equity Analyst",
            "Corporate Financial Manager",
            "Management Consultant",
            "Business Analyst",
            "Startup Founder / Entrepreneur"
        ],
        "stream_focus": "Commerce, Finance, Economics & Corporate Management"
    },
    "Humanities_HEC": {
        "id": "Humanities_HEC",
        "name": "Humanities / HEC (History, Economics, Civics / Arts)",
        "type": "class_10_stream",
        "description": "Empowers students passionate about societal dynamics, governance, literature, human behavior, legal systems, mass communication, and public administration.",
        "future_degrees": [
            "5-Year Integrated BA LLB / BBA LLB (Law)",
            "BA / B.Sc Psychology & Behavioral Sciences",
            "BA Journalism & Mass Communication",
            "BA Political Science / International Relations",
            "BA Public Policy & Civil Services Foundation"
        ],
        "future_careers": [
            "Corporate Lawyer / Advocate / Legal Advisor",
            "Clinical Psychologist / HR Behavioral Specialist",
            "Digital Journalist / Media Strategist / PR Director",
            "Civil Servant (IAS / IPS / IFS via UPSC)",
            "Public Policy Analyst / Think-Tank Researcher"
        ],
        "stream_focus": "Social Sciences, Law, Psychology, Communication & Public Policy"
    },

    # -------------------------------------------------------------
    # CLASS 12 DEGREE & CAREER PATHWAYS
    # -------------------------------------------------------------
    
    # --- Engineering & Tech Pathways (Require Math in 12th) ---
    "btech_cse": {
        "id": "btech_cse",
        "name": "B.Tech Computer Science & Engineering (CSE)",
        "type": "class_12_pathway",
        "category": "Engineering & Technology",
        "description": "Focuses on computer programming, algorithm design, software architecture, cloud platforms, cybersecurity, and scalable enterprise software.",
        "future_careers": ["Software Development Engineer (SDE)", "Backend Developer", "Cloud Solutions Architect", "Cybersecurity Specialist"],
        "top_skills": ["Data Structures & Algorithms", "System Design", "Python / Java / C++", "Cloud (AWS/GCP)"],
        "industry_demand": "Extremely High (Global Tech Sector Pillar)",
        "degree_duration": "4 Years"
    },
    "btech_aiml": {
        "id": "btech_aiml",
        "name": "B.Tech Artificial Intelligence & Data Science",
        "type": "class_12_pathway",
        "category": "Engineering & Technology",
        "description": "Specialized engineering pathway focusing on Machine Learning, Deep Learning, Big Data Engineering, Computer Vision, and Generative AI systems.",
        "future_careers": ["AI / Machine Learning Engineer", "Data Scientist", "Deep Learning Researcher", "NLP / Computer Vision Specialist"],
        "top_skills": ["Machine Learning (PyTorch/TensorFlow)", "Linear Algebra & Probability", "Python & SQL", "Data Pipeline Engineering"],
        "industry_demand": "Massive & Rapidly Expanding",
        "degree_duration": "4 Years"
    },
    "btech_ece": {
        "id": "btech_ece",
        "name": "B.Tech Electronics & Communication (ECE)",
        "type": "class_12_pathway",
        "category": "Engineering & Technology",
        "description": "Covers semiconductor chip design (VLSI), embedded microcontrollers, wireless communications (5G/6G), signal processing, and IoT hardware.",
        "future_careers": ["VLSI Chip Design Engineer", "Embedded Systems Engineer", "IoT Solutions Architect", "Telecom Specialist"],
        "top_skills": ["Verilog / VHDL & FPGA", "Embedded C", "Circuit Simulation & PCB", "Digital Signal Processing"],
        "industry_demand": "Very High (India Semiconductor Mission & Hardware Growth)",
        "degree_duration": "4 Years"
    },
    "btech_eee": {
        "id": "btech_eee",
        "name": "B.Tech Electrical & Electronics Engineering (EEE)",
        "type": "class_12_pathway",
        "category": "Engineering & Technology",
        "description": "Focuses on electric vehicle powertrains, battery management systems, renewable energy grids, smart power distribution, and power electronics.",
        "future_careers": ["Electric Vehicle (EV) Systems Engineer", "Power Grid Automation Engineer", "Renewable Energy Specialist", "Control Systems Designer"],
        "top_skills": ["Power Systems & Smart Grids", "EV Powertrain & BMS", "MATLAB & Simulink", "Control Automation"],
        "industry_demand": "High (Electric Mobility & Clean Green Energy Push)",
        "degree_duration": "4 Years"
    },
    "btech_mech": {
        "id": "btech_mech",
        "name": "B.Tech Mechanical Engineering & Robotics",
        "type": "class_12_pathway",
        "category": "Engineering & Technology",
        "description": "Covers mechanics, thermodynamics, robotics automation, automotive engineering, CAD/CAM manufacturing, and aerospace mechanical systems.",
        "future_careers": ["Mechanical Design Engineer", "Robotics & Automation Specialist", "Automotive R&D Engineer", "Aerospace Systems Analyst"],
        "top_skills": ["SolidWorks / AutoCAD / CATIA", "Thermodynamics & CFD", "Mechatronics & Robotics", "Finite Element Analysis (FEA)"],
        "industry_demand": "Steady, Essential & Expanding in Automation",
        "degree_duration": "4 Years"
    },
    "btech_civil": {
        "id": "btech_civil",
        "name": "B.Tech Civil Engineering & Smart Infrastructure",
        "type": "class_12_pathway",
        "category": "Engineering & Technology",
        "description": "Specializes in structural engineering, smart city urban planning, earthquake-resistant design, highway & metro transit networks, and environmental sustainability.",
        "future_careers": ["Structural Design Engineer", "Smart City Infrastructure Consultant", "Project Construction Manager", "Geotechnical Engineer"],
        "top_skills": ["Structural Analysis (STAAD Pro / ETABS)", "Building Information Modeling (BIM)", "Project Management & Estimation"],
        "industry_demand": "High (National Infrastructure & Urban Transit Projects)",
        "degree_duration": "4 Years"
    },

    # --- Medical & Clinical Healthcare Pathways (Require Biology in 12th) ---
    "mbbs_medicine": {
        "id": "mbbs_medicine",
        "name": "MBBS (Bachelor of Medicine, Bachelor of Surgery)",
        "type": "class_12_pathway",
        "category": "Medical & Clinical Healthcare",
        "description": "Premier medical degree in clinical medicine, surgical procedures, patient diagnosis, pharmacology, pathology, and healthcare management.",
        "future_careers": ["Medical Officer / Physician", "Specialist Doctor (MD/MS Surgeon, Cardiologist, Neurologist)", "Clinical Researcher", "Hospital Medical Director"],
        "top_skills": ["Human Anatomy & Physiology", "Clinical Diagnosis & Pathology", "Surgical Precision", "Patient Empathy & Crisis Care"],
        "industry_demand": "Extremely High & Prestigious",
        "degree_duration": "5.5 Years (including internship)"
    },
    "bds_dental": {
        "id": "bds_dental",
        "name": "BDS (Bachelor of Dental Surgery)",
        "type": "class_12_pathway",
        "category": "Medical & Clinical Healthcare",
        "description": "Specialized clinical degree in oral health, dental surgery, maxillofacial procedures, orthodontics, and restorative aesthetic dentistry.",
        "future_careers": ["Dentist / Dental Surgeon", "Orthodontist / Periodontist", "Dental Clinic Director", "Cosmetic Dental Consultant"],
        "top_skills": ["Oral Pathology & Radiology", "Surgical Dexterity", "Restorative Dentistry", "Patient Care"],
        "industry_demand": "High with Strong Independent Clinical Practice",
        "degree_duration": "5 Years"
    },
    "pharmacy": {
        "id": "pharmacy",
        "name": "B.Pharmacy / Pharm.D (Pharmaceutical Sciences)",
        "type": "class_12_pathway",
        "category": "Pharmaceutical & Life Sciences",
        "description": "Focuses on drug synthesis, medicinal chemistry, clinical trial monitoring, pharmacology, drug formulation, and pharmaceutical manufacturing.",
        "future_careers": ["Industrial Pharmacist", "Clinical Research Associate (CRA)", "Drug Formulation Scientist", "Drug Inspector / Regulatory Officer"],
        "top_skills": ["Medicinal Chemistry", "Pharmacokinetics", "Clinical Drug Protocols", "Regulatory Compliance (FDA/EMA)"],
        "industry_demand": "Very High (India is the Pharmacy of the World)",
        "degree_duration": "4 Years (B.Pharm) / 6 Years (Pharm.D)"
    },
    "biotechnology": {
        "id": "biotechnology",
        "name": "B.Sc / B.Tech Biotechnology",
        "type": "class_12_pathway",
        "category": "Interdisciplinary Life Sciences",
        "description": "Applies biological principles to industrial applications: CRISPR gene editing, recombinant DNA technology, vaccines, and agricultural biotechnology.",
        "future_careers": ["Biotech Research Scientist", "Genetic Engineer", "Bio-process Quality Engineer", "Agricultural Biotechnologist"],
        "top_skills": ["Molecular Biology Techniques", "Recombinant DNA & CRISPR", "Bioprocess Engineering", "Cell Culture Analysis"],
        "industry_demand": "High & Globally Expanding",
        "degree_duration": "3 to 4 Years"
    },
    "biomedical_science": {
        "id": "biomedical_science",
        "name": "Biomedical Science & Health Informatics",
        "type": "class_12_pathway",
        "category": "Healthcare Technology",
        "description": "Interdisciplinary field combining life sciences with modern computing, medical diagnostics, imaging technology, and electronic health record informatics.",
        "future_careers": ["Biomedical Diagnostics Specialist", "Health Informatics Analyst", "Medical Imaging Technologist", "Clinical Data Coordinator"],
        "top_skills": ["Medical Instrumentation", "Bio-Signal Analysis", "Clinical Data Systems", "Biochemical Diagnostics"],
        "industry_demand": "Rapidly Emerging in MedTech & Digital Health",
        "degree_duration": "3 to 4 Years"
    },
    "allied_health": {
        "id": "allied_health",
        "name": "B.Sc Nursing / Physiotherapy (BPT) / Allied Health",
        "type": "class_12_pathway",
        "category": "Medical & Clinical Healthcare",
        "description": "Critical clinical programs including Nursing, Physiotherapy, Medical Radiology & Imaging, and Medical Lab Technology supporting acute patient recovery.",
        "future_careers": ["Clinical Nurse Specialist", "Consultant Physiotherapist", "Radiology / MRI Technologist", "Medical Laboratory Director"],
        "top_skills": ["Patient Rehabilitation & Therapy", "Emergency & Critical Care", "Diagnostic Equipment Handling"],
        "industry_demand": "Immense Global Demand (India & Overseas)",
        "degree_duration": "4 to 4.5 Years"
    },
    "bioinformatics": {
        "id": "bioinformatics",
        "name": "B.Sc / B.Tech Bioinformatics & Computational Biology",
        "type": "class_12_pathway",
        "category": "Interdisciplinary Life Sciences",
        "description": "Bridges big data, programming, and biology to sequence DNA genomes, model protein 3D structures, and perform drug discovery simulations.",
        "future_careers": ["Bioinformatics Data Analyst", "Computational Biologist", "Genomic Data Scientist", "Structural Bio-Modeler"],
        "top_skills": ["Python / R for Biology", "Genomic Sequencing (NGS)", "Molecular Docking Tools", "Biostatistics"],
        "industry_demand": "High in Pharma R&D and Genomics Startups",
        "degree_duration": "3 to 4 Years"
    },

    # --- Commerce, Management & Finance Pathways ---
    "bcom_finance": {
        "id": "bcom_finance",
        "name": "B.Com Accounting & Corporate Finance",
        "type": "class_12_pathway",
        "category": "Commerce & Financial Services",
        "description": "Provides rigorous knowledge of financial accounting, corporate taxation, auditing standards, banking laws, and equity valuation.",
        "future_careers": ["Corporate Financial Accountant", "Statutory Auditor", "Taxation Consultant", "Commercial Banking Manager"],
        "top_skills": ["Financial Accounting & IFRS", "Corporate & Direct Tax Law", "Tally ERP / SAP & Advanced Excel", "Financial Reporting"],
        "industry_demand": "Universal & High Career Stability",
        "degree_duration": "3 Years"
    },
    "bba_management": {
        "id": "bba_management",
        "name": "BBA (Bachelor of Business Administration)",
        "type": "class_12_pathway",
        "category": "Business & Management",
        "description": "Prepares future managers and entrepreneurs in marketing strategy, operations management, HR, corporate strategy, and venture creation.",
        "future_careers": ["Management Executive", "Brand & Marketing Specialist", "Operations Manager", "Business Development Executive", "Startup Founder"],
        "top_skills": ["Strategic Leadership", "Marketing Analytics", "Operations & Supply Chain", "Business Communication"],
        "industry_demand": "High Across Corporate Sectors & Startups",
        "degree_duration": "3 Years"
    },
    "chartered_accountancy": {
        "id": "chartered_accountancy",
        "name": "Chartered Accountancy (CA) / CS / CMA",
        "type": "class_12_pathway",
        "category": "Professional Finance & Corporate Law",
        "description": "Prestigious professional certification covering advanced statutory auditing, forensic accounting, international taxation, and corporate governance.",
        "future_careers": ["Chartered Accountant (CA)", "Company Secretary (CS)", "Cost & Management Accountant", "CFO & Corporate Board Advisor"],
        "top_skills": ["Advanced Auditing & Assurance", "Direct & Indirect Tax Laws", "Financial Risk Management", "Company Law & Governance"],
        "industry_demand": "Top Tier Financial Prestige & Authority",
        "degree_duration": "4 to 5 Years"
    },
    "business_analytics": {
        "id": "business_analytics",
        "name": "BBA / B.Sc Business Analytics & FinTech",
        "type": "class_12_pathway",
        "category": "Business & Data Insights",
        "description": "Integrates quantitative data analytics, business intelligence dashboards, predictive modeling, and modern financial technology systems.",
        "future_careers": ["Business Analyst", "FinTech Product Associate", "Data Analytics Consultant", "Growth Marketing Analyst"],
        "top_skills": ["Data Visualization (PowerBI / Tableau)", "SQL & Business Analytics Python", "Financial Modeling & KPIs", "Predictive Analytics"],
        "industry_demand": "Very High in Data-Driven Enterprises",
        "degree_duration": "3 Years"
    },

    # --- Law, Humanities, Social Sciences & Public Policy ---
    "integrated_law": {
        "id": "integrated_law",
        "name": "5-Year Integrated Law (BA LLB / BBA LLB)",
        "type": "class_12_pathway",
        "category": "Law & Legal Services",
        "description": "Comprehensive professional law program covering Constitutional Law, Corporate Mergers & Acquisitions, Criminal Defense, Cyber Law, and IP Rights.",
        "future_careers": ["Corporate Legal Counsel", "High Court / Supreme Court Advocate", "Judicial Magistrate / Judge", "Cyber Law & IP Consultant"],
        "top_skills": ["Legal Research & Drafting", "Constitutional & Corporate Law", "Moot Court Oral Argumentation", "Contract Negotiation"],
        "industry_demand": "High Prestige & Lucrative Corporate Law Practice",
        "degree_duration": "5 Years"
    },
    "psychology": {
        "id": "psychology",
        "name": "BA / B.Sc Psychology & Behavioral Sciences",
        "type": "class_12_pathway",
        "category": "Behavioral Science & Mental Health",
        "description": "Studies human cognitive processes, neuro-psychology, clinical therapy, psychometric counseling, and organizational behavioral dynamics.",
        "future_careers": ["Clinical Psychologist / Counselor", "Organizational HR Behavioral Consultant", "Child & Educational Psychologist", "Neuro-psychology Researcher"],
        "top_skills": ["Psychological Assessment & Therapy", "Empathic Active Listening", "Behavioral Data Analysis", "Mental Health Intervention"],
        "industry_demand": "Rapidly Surging Awareness & Mental Health Demand",
        "degree_duration": "3 to 4 Years"
    },
    "journalism_communication": {
        "id": "journalism_communication",
        "name": "BA Journalism, Digital Media & Mass Communication",
        "type": "class_12_pathway",
        "category": "Media, Communication & PR",
        "description": "Covers digital multimedia journalism, broadcasting, corporate public relations, creative digital content strategy, and media ethics.",
        "future_careers": ["Digital Investigative Journalist", "Public Relations (PR) Director", "Multimedia Content Producer", "Corporate Brand Storyteller"],
        "top_skills": ["News Reporting & Editorial Writing", "Video / Podcast Digital Production", "Crisis PR Communication", "Social Media Strategy"],
        "industry_demand": "High in Digital Media, OTT, and Corporate PR",
        "degree_duration": "3 Years"
    },
    "public_policy_civil_services": {
        "id": "public_policy_civil_services",
        "name": "Social Sciences, Public Policy & Civil Services (UPSC)",
        "type": "class_12_pathway",
        "category": "Public Governance & Social Impact",
        "description": "Provides solid academic foundation in Political Science, Economics, Public Administration, and Sociology for UPSC Civil Services and policy think tanks.",
        "future_careers": ["Civil Services Officer (IAS / IPS / IFS)", "Public Policy Analyst", "International NGO Program Director", "Socio-Economic Researcher"],
        "top_skills": ["Public Administration & Governance", "Policy Research & Impact Evaluation", "Socio-Economic Analysis", "Constitutional Frameworks"],
        "industry_demand": "High National Impact & Leadership Authority",
        "degree_duration": "3 Years"
    }
}
