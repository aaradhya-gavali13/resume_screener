import os
import io
import re
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
from docx import Document

# ============================================================
# JOB ROLE DATABASE
# ============================================================

JOB_ROLES = {
    "Data Analyst": {
        "category": "Data & AI",
        "description": "Transforms raw data into actionable business intelligence, dashboards, and strategic insights.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "MBA"],
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
        "category": "Data & AI",
        "description": "Designs mathematical models, predictive algorithms, and statistical systems.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "Data & AI",
        "description": "Productionizes ML pipelines, trains neural architectures, and deploys high-throughput models.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "Data & AI",
        "description": "Builds next-gen cognitive services with LLMs, Generative AI, and Computer Vision.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "Data & AI",
        "description": "Architects scalable real-time and batch data pipelines, lakes, and warehouses.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "DevOps & Cloud",
        "description": "Bridges machine learning and operations with automated CI/CD for models and artifact registries.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "Core Engineering",
        "description": "Constructs robust, maintainable software systems with clean architecture and design patterns.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "Core Engineering",
        "description": "Engineers clean, high-performance backends, microservices, and APIs exclusively with Python.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"],
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
        "category": "Web & Fullstack",
        "description": "Commands the entire web stack from responsive frontends to scalable databases and cloud APIs.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"],
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
        "category": "Web & Fullstack",
        "description": "Crafts ultra-responsive, beautiful, high-speed user interfaces and web applications.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA"],
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
        "category": "Web & Fullstack",
        "description": "Specializes in servers, high-throughput databases, microservices architecture, and security.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"],
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
        "category": "DevOps & Cloud",
        "description": "Automates continuous delivery pipelines, infrastructure as code, and cluster orchestration.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "DevOps & Cloud",
        "description": "Designs resilient multi-cloud infrastructures, network topography, and serverless architectures.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
        "category": "Security",
        "description": "Guards network frontiers, performs penetration audits, and neutralizes adversarial threats.",
        "programs": ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
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
# SKILL & PROGRAM ALIASES
# ============================================================

ALIASES = {
    "python3": "Python",
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "powerbi": "Power BI",
    "power-bi": "Power BI",
    "ml": "Machine Learning",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "dl": "Deep Learning",
    "gen ai": "Generative AI",
    "genai": "Generative AI",
    "generative artificial intelligence": "Generative AI",
    "large language model": "LLM",
    "large language models": "LLM",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "computer vision": "Computer Vision",
    "opencv": "OpenCV",
    "open cv": "OpenCV",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",
    "k8s": "Kubernetes",
    "amazon web services": "AWS",
    "microsoft azure": "Azure",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    "continuous integration": "CI/CD",
    "continuous deployment": "CI/CD",
    "continuous integration and continuous deployment": "CI/CD",
    "github": "Git",
    "gitlab": "Git",
    "rest apis": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "data structure": "Data Structures",
    "algorithm": "Algorithms",
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",
    "extract transform load": "ETL",
    "extract-transform-load": "ETL",
    "spark": "Apache Spark",
    "airflow": "Apache Airflow",
    "pyspark": "PySpark",
    "kafka": "Kafka",
    "docker": "Docker",
    "linux": "Linux",
    "bash shell": "Bash",
    "tableau": "Tableau"
}

PROGRAM_ALIASES = {
    "bca": "BCA",
    "b.c.a": "BCA",
    "bachelor of computer applications": "BCA",
    "bachelor in computer applications": "BCA",
    "bsc": "B.Sc",
    "b.sc": "B.Sc",
    "bachelor of science": "B.Sc",
    "btech": "B.Tech",
    "b.tech": "B.Tech",
    "bachelor of technology": "B.Tech",
    "be": "BE",
    "b.e": "BE",
    "b.e.": "BE",
    "bachelor of engineering": "BE",
    "mca": "MCA",
    "m.c.a": "MCA",
    "master of computer applications": "MCA",
    "msc": "M.Sc",
    "m.sc": "M.Sc",
    "master of science": "M.Sc",
    "mtech": "M.Tech",
    "m.tech": "M.Tech",
    "master of technology": "M.Tech",
    "mba": "MBA",
    "m.b.a": "MBA",
    "master of business administration": "MBA"
}

# ============================================================
# PARSING & MATCHING LOGIC
# ============================================================

def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def detect_programs(text: str) -> List[str]:
    normalized = normalize_text(text)
    detected = set()
    for alias, standard in PROGRAM_ALIASES.items():
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        if re.search(pattern, normalized):
            detected.add(standard)
    return sorted(list(detected))

def detect_skills(text: str) -> List[str]:
    normalized = normalize_text(text)
    detected = set()

    for alias, standard in ALIASES.items():
        pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
        if re.search(pattern, normalized):
            detected.add(standard)

    all_skills = set()
    for role_data in JOB_ROLES.values():
        for skill in role_data["skills"]:
            all_skills.add(skill)

    for skill in all_skills:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, normalized):
            detected.add(skill)

    return sorted(list(detected))

def get_tier(score: float) -> Dict[str, str]:
    if score >= 85:
        return {"name": "S-TIER", "class": "tier-s", "glow": "#00f0ff"}
    elif score >= 70:
        return {"name": "A-TIER", "class": "tier-a", "glow": "#10b981"}
    elif score >= 55:
        return {"name": "B-TIER", "class": "tier-b", "glow": "#a855f7"}
    elif score >= 40:
        return {"name": "C-TIER", "class": "tier-c", "glow": "#f59e0b"}
    return {"name": "D-TIER", "class": "tier-d", "glow": "#ef4444"}

def calculate_role_score(candidate_skills: List[str], candidate_programs: List[str], role_data: dict) -> dict:
    role_skills = role_data["skills"]
    total_weight = sum(role_skills.values())

    matched_skills = []
    missing_skills = []
    raw_score = 0

    for skill, weight in role_skills.items():
        if skill in candidate_skills:
            matched_skills.append(skill)
            raw_score += weight
        else:
            missing_skills.append({"skill": skill, "weight": weight})

    skill_score = (raw_score / total_weight) * 100 if total_weight else 0

    education_match = any(prog in candidate_programs for prog in role_data["programs"])
    education_score = 5 if education_match else 0
    final_score = min(100.0, (skill_score * 0.95) + education_score)

    missing_skills.sort(key=lambda x: x["weight"], reverse=True)

    # Human-friendly color-diversified priority roadmaps (NO raw backend weights)
    improvements = []
    for idx, item in enumerate(missing_skills[:5]):
        w = item["weight"]
        if w >= 12 or (idx == 0 and w >= 10):
            p_level = "Critical Priority"
            p_class = "priority-critical"
        elif w >= 8:
            p_level = "High Priority"
            p_class = "priority-high"
        elif w >= 4:
            p_level = "Medium Priority"
            p_class = "priority-medium"
        else:
            p_level = "Recommended"
            p_class = "priority-recommended"

        improvements.append({
            "skill": item["skill"],
            "priorityLevel": p_level,
            "priorityClass": p_class,
            "action": f"Learn {item['skill']}"
        })

    return {
        "score": round(final_score, 2),
        "skillScore": round(skill_score, 2),
        "matchedSkills": sorted(matched_skills),
        "missingSkills": [m["skill"] for m in missing_skills],
        "allMissingDetails": missing_skills,
        "improvements": improvements,
        "educationMatch": education_match,
        "tier": get_tier(final_score)
    }

def run_analysis(text: str) -> dict:
    candidate_skills = detect_skills(text)
    candidate_programs = detect_programs(text)

    all_roles = []
    for role, role_data in JOB_ROLES.items():
        res = calculate_role_score(candidate_skills, candidate_programs, role_data)
        res["role"] = role
        res["category"] = role_data["category"]
        res["description"] = role_data["description"]
        all_roles.append(res)

    all_roles.sort(key=lambda x: x["score"], reverse=True)

    return {
        "candidateSkills": candidate_skills,
        "candidatePrograms": candidate_programs,
        "topRoles": all_roles[:5],
        "allRoles": all_roles,
        "textLength": len(text),
        "wordCount": len(text.strip().split())
    }

# ============================================================
# FASTAPI APPLICATION & CORS
# ============================================================

app = FastAPI(
    title="NEXUS RESUME AI - Backend API",
    description="Futuristic Resume & Role Compatibility Analysis Engine",
    version="2.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextPayload(BaseModel):
    text: str

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "nexus-resume-ai-backend",
        "version": "2.5.0",
        "roles_available": len(JOB_ROLES)
    }

@app.post("/analyze")
async def analyze_endpoint(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    extracted_text = ""

    if file:
        filename = file.filename.lower()
        content = await file.read()

        if filename.endswith(".pdf"):
            try:
                reader = PdfReader(io.BytesIO(content))
                pages_text = [page.extract_text() or "" for page in reader.pages]
                extracted_text = "\n".join(pages_text)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"PDF extraction error: {str(e)}")
        elif filename.endswith(".docx"):
            try:
                doc = Document(io.BytesIO(content))
                paragraphs_text = [p.text for p in doc.paragraphs]
                extracted_text = "\n".join(paragraphs_text)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"DOCX extraction error: {str(e)}")
        elif filename.endswith(".txt"):
            try:
                extracted_text = content.decode("utf-8", errors="ignore")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"TXT extraction error: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, or TXT.")

    elif text:
        extracted_text = text
    else:
        raise HTTPException(status_code=400, detail="No resume file or text provided.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the provided resume.")

    return run_analysis(extracted_text)

@app.post("/analyze-json")
def analyze_json(payload: TextPayload):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")
    return run_analysis(payload.text)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
