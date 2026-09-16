import os
import re

from pypdf import PdfReader
from docx import Document


# ============================================================
# JOB ROLE DATABASE
# ============================================================

JOB_ROLES = {

    "Data Analyst": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "MBA"
        ],

        "skills": {
            "SQL": 18,
            "Excel": 14,
            "Python": 12,
            "Data Analysis": 10,
            "Statistics": 10,
            "Power BI": 10,
            "Data Visualization": 6,
            "Pandas": 5,
            "Business Analytics": 5,
            "Financial Analytics": 3,
            "Marketing Analytics": 2,
            "Sales Analytics": 2,
            "Customer Analytics": 2,
            "Operations Analytics": 1
        }
    },


    "Data Scientist": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Python": 15,
            "Machine Learning": 15,
            "Statistics": 12,
            "SQL": 10,
            "Pandas": 7,
            "NumPy": 5,
            "Scikit-learn": 8,
            "Data Analysis": 5,
            "Data Visualization": 5,
            "Deep Learning": 8,
            "TensorFlow": 5,
            "PyTorch": 5
        }
    },


    "Machine Learning Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Python": 15,
            "Machine Learning": 15,
            "Scikit-learn": 10,
            "Deep Learning": 12,
            "TensorFlow": 7,
            "PyTorch": 7,
            "SQL": 5,
            "Pandas": 5,
            "NumPy": 5,
            "Feature Engineering": 7,
            "Model Deployment": 5,
            "MLOps": 7
        }
    },


    "AI Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Python": 15,
            "Machine Learning": 10,
            "Deep Learning": 15,
            "TensorFlow": 8,
            "PyTorch": 8,
            "NLP": 8,
            "Computer Vision": 8,
            "Generative AI": 8,
            "LLM": 7,
            "SQL": 4,
            "OpenCV": 4,
            "Model Deployment": 5
        }
    },


    "Data Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "SQL": 15,
            "Python": 12,
            "ETL": 12,
            "Data Pipelines": 10,
            "Data Warehousing": 8,
            "Apache Spark": 8,
            "Apache Airflow": 7,
            "AWS": 7,
            "Azure": 5,
            "GCP": 5,
            "PySpark": 6,
            "Kafka": 5
        }
    },


    "MLOps Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Python": 12,
            "Machine Learning": 10,
            "MLOps": 15,
            "Docker": 10,
            "Kubernetes": 10,
            "AWS": 8,
            "Azure": 5,
            "CI/CD": 8,
            "Git": 5,
            "MLflow": 7,
            "Linux": 5,
            "Model Deployment": 5
        }
    },


    "Software Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Python": 8,
            "Java": 12,
            "C++": 10,
            "JavaScript": 10,
            "Data Structures": 12,
            "Algorithms": 10,
            "OOP": 8,
            "Git": 5,
            "SQL": 5,
            "REST API": 5,
            "Problem Solving": 5
        }
    },


    "Python Developer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"
        ],

        "skills": {
            "Python": 25,
            "Django": 10,
            "Flask": 8,
            "FastAPI": 8,
            "REST API": 8,
            "SQL": 10,
            "Git": 5,
            "OOP": 8,
            "Data Structures": 8,
            "Docker": 5,
            "JavaScript": 5
        }
    },


    "Full Stack Developer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"
        ],

        "skills": {
            "HTML": 5,
            "CSS": 5,
            "JavaScript": 12,
            "React": 10,
            "Node.js": 10,
            "Express.js": 7,
            "Python": 5,
            "Java": 5,
            "SQL": 8,
            "MongoDB": 8,
            "REST API": 7,
            "Git": 5,
            "Docker": 3,
            "TypeScript": 5
        }
    },


    "Frontend Developer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA"
        ],

        "skills": {
            "HTML": 12,
            "CSS": 12,
            "JavaScript": 18,
            "React": 15,
            "TypeScript": 8,
            "Next.js": 7,
            "Tailwind CSS": 5,
            "Git": 5,
            "REST API": 5,
            "Responsive Design": 8,
            "UI Development": 5
        }
    },


    "Backend Developer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"
        ],

        "skills": {
            "Python": 10,
            "Java": 10,
            "Node.js": 10,
            "Django": 7,
            "Flask": 7,
            "FastAPI": 7,
            "SQL": 12,
            "PostgreSQL": 7,
            "MySQL": 5,
            "REST API": 10,
            "Docker": 5,
            "Git": 5,
            "Microservices": 5
        }
    },


    "DevOps Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Linux": 10,
            "Docker": 12,
            "Kubernetes": 12,
            "AWS": 10,
            "Azure": 7,
            "CI/CD": 10,
            "Jenkins": 7,
            "Git": 7,
            "Terraform": 7,
            "Ansible": 5,
            "Python": 5,
            "Bash": 8
        }
    },


    "Cloud Engineer": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "AWS": 20,
            "Azure": 10,
            "GCP": 10,
            "Cloud Computing": 10,
            "Docker": 10,
            "Kubernetes": 10,
            "Linux": 8,
            "Networking": 7,
            "Terraform": 5,
            "Python": 5,
            "CI/CD": 5
        }
    },


    "Cybersecurity Analyst": {
        "programs": [
            "BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"
        ],

        "skills": {
            "Cybersecurity": 15,
            "Networking": 12,
            "Linux": 10,
            "Python": 8,
            "Ethical Hacking": 10,
            "Penetration Testing": 10,
            "SIEM": 8,
            "Firewalls": 7,
            "Cryptography": 7,
            "Incident Response": 7,
            "Threat Analysis": 6
        }
    }
}


# ============================================================
# SKILL ALIASES
# ============================================================

ALIASES = {

    # Python
    "python3": "Python",

    # Excel
    "ms excel": "Excel",
    "microsoft excel": "Excel",

    # Power BI
    "powerbi": "Power BI",
    "power-bi": "Power BI",

    # Machine Learning
    "ml": "Machine Learning",

    # Scikit-learn
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",

    # Deep Learning
    "dl": "Deep Learning",

    # Generative AI
    "gen ai": "Generative AI",
    "genai": "Generative AI",
    "generative artificial intelligence": "Generative AI",

    # LLM
    "large language model": "LLM",
    "large language models": "LLM",

    # NLP
    "natural language processing": "NLP",

    # Computer Vision
    "computer vision": "Computer Vision",

    # OpenCV
    "opencv": "OpenCV",
    "open cv": "OpenCV",

    # Node.js
    "nodejs": "Node.js",
    "node.js": "Node.js",

    # Express
    "express": "Express.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",

    # Kubernetes
    "k8s": "Kubernetes",

    # AWS
    "amazon web services": "AWS",

    # Azure
    "microsoft azure": "Azure",

    # GCP
    "google cloud": "GCP",
    "google cloud platform": "GCP",

    # CI/CD
    "continuous integration": "CI/CD",
    "continuous deployment": "CI/CD",
    "continuous integration and continuous deployment": "CI/CD",

    # Git
    "github": "Git",
    "gitlab": "Git",

    # REST API
    "rest apis": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",

    # SQL databases
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "mysql": "MySQL",

    # Data structures
    "data structure": "Data Structures",

    # Algorithms
    "algorithm": "Algorithms",

    # OOP
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",

    # ETL
    "extract transform load": "ETL",
    "extract-transform-load": "ETL",

    # Spark
    "spark": "Apache Spark",

    # Airflow
    "airflow": "Apache Airflow",

    # PySpark
    "pyspark": "PySpark",

    # Kafka
    "apache kafka": "Kafka",

    # Docker
    "docker": "Docker",

    # Linux
    "linux": "Linux",

    # Bash
    "bash shell": "Bash"
}


# ============================================================
# PROGRAM / DEGREE ALIASES
# ============================================================

PROGRAM_ALIASES = {

    # BCA
    "bca": "BCA",
    "b.c.a": "BCA",
    "bachelor of computer applications": "BCA",
    "bachelor in computer applications": "BCA",

    # B.Sc
    "bsc": "B.Sc",
    "b.sc": "B.Sc",
    "bachelor of science": "B.Sc",

    # B.Tech
    "btech": "B.Tech",
    "b.tech": "B.Tech",
    "bachelor of technology": "B.Tech",

    # BE
    "be": "BE",
    "b.e": "BE",
    "b.e.": "BE",
    "bachelor of engineering": "BE",

    # MCA
    "mca": "MCA",
    "m.c.a": "MCA",
    "master of computer applications": "MCA",

    # M.Sc
    "msc": "M.Sc",
    "m.sc": "M.Sc",
    "master of science": "M.Sc",

    # M.Tech
    "mtech": "M.Tech",
    "m.tech": "M.Tech",
    "master of technology": "M.Tech",

    # MBA
    "mba": "MBA",
    "m.b.a": "MBA",
    "master of business administration": "MBA"
}


# ============================================================
# READ PDF
# ============================================================

def read_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text() or ""

        text += page_text + "\n"

    return text


# ============================================================
# READ DOCX
# ============================================================

def read_docx(path):

    doc = Document(path)

    text = ""

    for paragraph in doc.paragraphs:

        text += paragraph.text + "\n"

    return text


# ============================================================
# READ TXT
# ============================================================

def read_txt(path):

    with open(path, "r", encoding="utf-8") as file:

        return file.read()


# ============================================================
# MAIN FILE READER
# ============================================================

def read_resume(path):

    extension = os.path.splitext(path)[1].lower()

    if extension == ".pdf":

        return read_pdf(path)

    elif extension == ".docx":

        return read_docx(path)

    elif extension == ".txt":

        return read_txt(path)

    else:

        raise ValueError(
            "Unsupported file format. Use PDF, DOCX or TXT."
        )


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# DETECT PROGRAMS
# ============================================================

def detect_programs(text):

    normalized = normalize_text(text)

    detected_programs = set()

    for alias, standard_program in PROGRAM_ALIASES.items():

        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

        if re.search(pattern, normalized):

            detected_programs.add(standard_program)

    return sorted(detected_programs)


# ============================================================
# DETECT SKILLS
# ============================================================

def detect_skills(text):

    normalized = normalize_text(text)

    detected_skills = set()

    # --------------------------------------------------------
    # First detect aliases
    # --------------------------------------------------------

    for alias, standard_skill in ALIASES.items():

        pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"

        if re.search(pattern, normalized):

            detected_skills.add(standard_skill)

    # --------------------------------------------------------
    # Then detect normal skill names
    # --------------------------------------------------------

    all_skills = set()

    for role_data in JOB_ROLES.values():

        for skill in role_data["skills"]:

            all_skills.add(skill)

    for skill in all_skills:

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, normalized):

            detected_skills.add(skill)

    return sorted(detected_skills)


# ============================================================
# CHECK PROGRAM ELIGIBILITY
# ============================================================

def check_program_eligibility(
    detected_programs,
    required_programs
):

    for program in required_programs:

        if program in detected_programs:

            return True, program

    return False, None


# ============================================================
# CALCULATE ROLE SCORE
# ============================================================

def calculate_role_score(
    role_name,
    role_data,
    detected_skills
):

    skill_weights = role_data["skills"]

    total_weight = sum(skill_weights.values())

    matched_skills = []
    missing_skills = []

    raw_score = 0

    # --------------------------------------------------------
    # Compare every required skill
    # --------------------------------------------------------

    for skill, weight in skill_weights.items():

        if skill in detected_skills:

            matched_skills.append(skill)

            raw_score += weight

        else:

            missing_skills.append(
                {
                    "skill": skill,
                    "weight": weight
                }
            )

    # --------------------------------------------------------
    # Normalize score to 100
    # --------------------------------------------------------

    if total_weight > 0:

        score = (raw_score / total_weight) * 100

    else:

        score = 0

    score = round(score, 2)

    # --------------------------------------------------------
    # Sort missing skills by importance
    # --------------------------------------------------------

    missing_skills.sort(
        key=lambda x: x["weight"],
        reverse=True
    )

    # Top 5 skills to improve
    priority_missing = missing_skills[:5]

    return {
        "role": role_name,
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": [
            item["skill"]
            for item in missing_skills
        ],
        "priority_missing": [
            item["skill"]
            for item in priority_missing
        ]
    }


# ============================================================
# FIND TOP ELIGIBLE ROLES
# ============================================================

def find_top_roles(
    detected_programs,
    detected_skills
):

    results = []

    for role_name, role_data in JOB_ROLES.items():

        required_programs = role_data["programs"]

        # ====================================================
        # STEP 1: PROGRAM CHECK
        # ====================================================

        eligible, matched_program = check_program_eligibility(
            detected_programs,
            required_programs
        )

        # ----------------------------------------------------
        # If program doesn't match, completely skip role
        # ----------------------------------------------------

        if not eligible:

            continue

        # ====================================================
        # STEP 2: ONLY NOW CALCULATE SKILL SCORE
        # ====================================================

        result = calculate_role_score(
            role_name,
            role_data,
            detected_skills
        )

        result["eligible"] = True

        result["matched_program"] = matched_program

        result["required_programs"] = required_programs

        results.append(result)

    # ========================================================
    # SORT ELIGIBLE ROLES BY SCORE
    # ========================================================

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # ========================================================
    # RETURN TOP 5
    # ========================================================

    return results[:5]


# ============================================================
# PRINT RESULTS
# ============================================================

def print_results(
    detected_programs,
    detected_skills,
    results
):

    print("\n")
    print("=" * 70)
    print("CAREERFIT AI - RESUME ANALYSIS")
    print("=" * 70)

    print("\nDetected Programs:")

    if detected_programs:

        for program in detected_programs:

            print(f"  ✓ {program}")

    else:

        print("  No recognized program found.")

    print("\nDetected Skills:")

    if detected_skills:

        for skill in detected_skills:

            print(f"  ✓ {skill}")

    else:

        print("  No recognized skills found.")

    print("\n")
    print("=" * 70)
    print("TOP ELIGIBLE CAREER ROLES")
    print("=" * 70)

    if not results:

        print(
            "\nNo eligible roles found based on the "
            "recognized educational program."
        )

        return

    for index, result in enumerate(results, start=1):

        print("\n" + "-" * 70)

        print(
            f"{index}. {result['role']}"
        )

        print(
            f"Eligibility: ELIGIBLE"
        )

        print(
            f"Program Match: {result['matched_program']}"
        )

        print(
            f"Skill Match Score: {result['score']}/100"
        )

        # ----------------------------------------------------
        # Matched skills
        # ----------------------------------------------------

        print("\nMatched Skills:")

        if result["matched_skills"]:

            for skill in result["matched_skills"]:

                print(f"  ✓ {skill}")

        else:

            print("  None")

        # ----------------------------------------------------
        # Missing skills
        # ----------------------------------------------------

        print("\nMissing Skills:")

        if result["missing_skills"]:

            for skill in result["missing_skills"]:

                print(f"  ✗ {skill}")

        else:

            print("  None")

        # ----------------------------------------------------
        # Priority improvements
        # ----------------------------------------------------

        print("\nPriority Improvements:")

        if result["priority_missing"]:

            for skill in result["priority_missing"]:

                print(f"  → Learn/Improve {skill}")

        else:

            print("  No major missing skills.")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("CAREERFIT AI - RESUME CAREER RECOMMENDER")
    print("=" * 70)

    path = input(
        "\nEnter resume file path: "
    ).strip().strip('"')

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not os.path.exists(path):

        print("\nERROR: File does not exist.")

        return

    try:

        # ====================================================
        # 1. READ RESUME
        # ====================================================

        text = read_resume(path)

        if not text.strip():

            print(
                "\nERROR: Could not extract text from resume."
            )

            return

        # ====================================================
        # 2. NORMALIZE
        # ====================================================

        text = normalize_text(text)

        # ====================================================
        # 3. DETECT PROGRAM
        # ====================================================

        detected_programs = detect_programs(text)

        # ====================================================
        # 4. DETECT SKILLS
        # ====================================================

        detected_skills = detect_skills(text)

        # ====================================================
        # 5. PROGRAM FIRST
        # 6. SKILL SCORE SECOND
        # ====================================================

        results = find_top_roles(
            detected_programs,
            detected_skills
        )

        # ====================================================
        # 7. DISPLAY
        # ====================================================

        print_results(
            detected_programs,
            detected_skills,
            results
        )

    except Exception as e:

        print("\nERROR:")
        print(e)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()