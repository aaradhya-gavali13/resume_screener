/**
 * NEXUS RESUME AI - CORE QUANTUM MATCH ENGINE
 * Ported from questions.py with enhanced telemetry & browser-based parser
 */

// =========================================================
// JOB ROLES DATABASE
// =========================================================
const JOB_ROLES = {
  "Data Analyst": {
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "MBA"],
    category: "Data & AI",
    description: "Transforms raw data into actionable business intelligence, dashboards, and strategic insights.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "Data & AI",
    description: "Designs mathematical models, predictive algorithms, and statistical systems to solve complex problems.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "Data & AI",
    description: "Productionizes ML pipelines, trains neural architectures, and deploys high-throughput models.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "Data & AI",
    description: "Builds next-gen cognitive services with LLMs, Generative AI, Computer Vision, and agentic workflows.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "Data & AI",
    description: "Architects scalable real-time and batch data pipelines, lakes, warehouses, and stream processors.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "DevOps & Cloud",
    description: "Bridges machine learning and operations with CI/CD for models, artifact registries, and monitoring.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "Core Engineering",
    description: "Constructs robust, maintainable software systems with clean code, algorithms, and design patterns.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"],
    category: "Core Engineering",
    description: "Engineers clean, high-performance backends, automation tools, and APIs exclusively with Python.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"],
    category: "Web & Fullstack",
    description: "Commands the entire web stack from responsive frontends to scalable databases and cloud APIs.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA"],
    category: "Web & Fullstack",
    description: "Crafts ultra-responsive, beautiful, high-speed user interfaces and web applications.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc"],
    category: "Web & Fullstack",
    description: "Specializes in servers, high-throughput databases, microservices architecture, and security protocols.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "DevOps & Cloud",
    description: "Automates continuous delivery pipelines, infrastructure as code, containerization, and cluster health.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "DevOps & Cloud",
    description: "Designs resilient multi-cloud infrastructures, network topography, and serverless topologies.",
    skills: {
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
    programs: ["BCA", "B.Sc", "B.Tech", "BE", "MCA", "M.Sc", "M.Tech"],
    category: "Security",
    description: "Guards network frontiers, performs penetration audits, and neutralizes adversarial threats.",
    skills: {
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
};

// =========================================================
// SKILL ALIASES DICTIONARY
// =========================================================
const ALIASES = {
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
};

// =========================================================
// PROGRAM ALIASES DICTIONARY
// =========================================================
const PROGRAM_ALIASES = {
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
};

// =========================================================
// SAMPLE RESUME TEXT
// =========================================================
const SAMPLE_RESUME_TEXT = `
AARADHYA SHARMA
Email: aaradhya.sharma@example.com | Phone: +91 98765 43210
Portfolio: github.com/aaradhya-analyst | LinkedIn: linkedin.com/in/aaradhya-data

EDUCATION:
Bachelor of Computer Applications (BCA) - Distinction
CGPA: 8.9 / 10 | 2021 - 2024

PROFESSIONAL SUMMARY:
Results-driven BCA graduate with deep competence in Data Analysis, statistical modeling, and business intelligence. Proven track record constructing automated SQL pipelines, dynamic interactive dashboards in Power BI and Tableau, and exploratory quantitative analysis using Python, Pandas, and NumPy.

TECHNICAL SKILLS:
- Languages & Querying: Python, SQL, PostgreSQL, MySQL
- Data Analysis & Libraries: Data Analysis, Pandas, NumPy, Statistics, Data Visualization
- Business Intelligence: Power BI, Tableau, Excel (Advanced formulas, Pivot tables, VLOOKUP)
- Developer Tools: Git, GitHub

KEY PROJECTS:
1. Retail Sales & Customer Retention Analytics:
- Extracted and cleaned 500K+ transactional records using PostgreSQL and Python (Pandas).
- Created statistical models and executive reporting dashboards in Power BI and Tableau.
- Derived KPI insights that boosted customer cohort retention by 18%.

2. Financial Market Volatility Visualizer:
- Built an automated pipeline ingesting daily stock metrics using SQL and Python.
- Leveraged NumPy and Statistics to compute rolling risk metrics and variance.
- Visualized trend patterns using Data Visualization best practices.
`;

// =========================================================
// WEB AUDIO SOUND SYNTHESIZER (CYBER AUDIO FX)
// =========================================================
class CyberAudio {
  constructor() {
    this.enabled = true;
    this.ctx = null;
  }

  init() {
    if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
  }

  playTone(freq, type, duration, vol = 0.05) {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(vol, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      // Audio might be blocked by browser policy until interaction
    }
  }

  scanBleep() {
    this.playTone(880, 'sine', 0.08, 0.03);
    setTimeout(() => this.playTone(1320, 'sine', 0.08, 0.03), 90);
  }

  successChime() {
    this.playTone(523.25, 'triangle', 0.15, 0.05);
    setTimeout(() => this.playTone(659.25, 'triangle', 0.15, 0.05), 100);
    setTimeout(() => this.playTone(783.99, 'triangle', 0.25, 0.05), 200);
    setTimeout(() => this.playTone(1046.50, 'sine', 0.35, 0.06), 320);
  }

  clickBlip() {
    this.playTone(1200, 'square', 0.03, 0.015);
  }
}

const audio = new CyberAudio();

// =========================================================
// TEXT NORMALIZATION & PARSING
// =========================================================
function normalizeText(text) {
  let normalized = text.toLowerCase();
  normalized = normalized.replace(/[–—]/g, "-");
  normalized = normalized.replace(/\s+/g, " ");
  return normalized.trim();
}

function detectPrograms(text) {
  const normalized = normalizeText(text);
  const detected = new Set();

  for (const [alias, standardProgram] of Object.entries(PROGRAM_ALIASES)) {
    // Regex boundary matching: (?<!\w)alias(?!\w)
    const escaped = alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(?:^|[^a-zA-Z0-9])${escaped}(?:$|[^a-zA-Z0-9])`, 'i');
    if (regex.test(normalized)) {
      detected.add(standardProgram);
    }
  }
  return Array.from(detected).sort();
}

function detectSkills(text) {
  const normalized = normalizeText(text);
  const detected = new Set();

  // 1. Detect aliases
  for (const [alias, standardSkill] of Object.entries(ALIASES)) {
    const escaped = alias.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(?:^|[^a-zA-Z0-9])${escaped}(?:$|[^a-zA-Z0-9])`, 'i');
    if (regex.test(normalized)) {
      detected.add(standardSkill);
    }
  }

  // 2. Detect normal skill names from all job roles
  const allSkills = new Set();
  for (const roleData of Object.values(JOB_ROLES)) {
    for (const skill of Object.keys(roleData.skills)) {
      allSkills.add(skill);
    }
  }

  for (const skill of allSkills) {
    const escaped = skill.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(?:^|[^a-zA-Z0-9])${escaped}(?:$|[^a-zA-Z0-9])`, 'i');
    if (regex.test(normalized)) {
      detected.add(skill);
    }
  }

  return Array.from(detected).sort();
}

// =========================================================
// CALCULATE ROLE SCORE & RANKINGS
// =========================================================
function calculateRoleScore(candidateSkills, candidatePrograms, roleData) {
  const roleSkills = roleData.skills;
  const totalWeight = Object.values(roleSkills).reduce((a, b) => a + b, 0);

  const matchedSkills = [];
  const missingSkills = [];
  let rawScore = 0;

  for (const [skill, weight] of Object.entries(roleSkills)) {
    if (candidateSkills.includes(skill)) {
      matchedSkills.push(skill);
      rawScore += weight;
    } else {
      missingSkills.push({ skill, weight });
    }
  }

  const skillScore = totalWeight ? (rawScore / totalWeight) * 100 : 0;

  // Education match
  let educationMatch = false;
  for (const program of roleData.programs) {
    if (candidatePrograms.includes(program)) {
      educationMatch = true;
      break;
    }
  }

  const educationScore = educationMatch ? 5 : 0;
  const finalScore = Math.min(100, (skillScore * 0.95) + educationScore);

  // Sort missing skills by priority
  missingSkills.sort((a, b) => b.weight - a.weight);

  const improvements = missingSkills.slice(0, 5).map((item, index) => {
    let priorityLevel = "Recommended";
    let priorityClass = "priority-recommended";

    if (item.weight >= 12 || (index === 0 && item.weight >= 10)) {
      priorityLevel = "Critical Priority";
      priorityClass = "priority-critical";
    } else if (item.weight >= 8) {
      priorityLevel = "High Priority";
      priorityClass = "priority-high";
    } else if (item.weight >= 4) {
      priorityLevel = "Medium Priority";
      priorityClass = "priority-medium";
    }

    return {
      skill: item.skill,
      priorityLevel: priorityLevel,
      priorityClass: priorityClass,
      action: `Learn ${item.skill}`
    };
  });

  return {
    score: Math.round(finalScore * 100) / 100,
    skillScore: Math.round(skillScore * 100) / 100,
    matchedSkills: matchedSkills.sort(),
    missingSkills: missingSkills.map(m => m.skill),
    allMissingDetails: missingSkills,
    improvements: improvements,
    educationMatch: educationMatch,
    tier: getTierBadge(finalScore)
  };
}

function getTierBadge(score) {
  if (score >= 85) return { name: "S-TIER", class: "tier-s", glow: "#00f0ff" };
  if (score >= 70) return { name: "A-TIER", class: "tier-a", glow: "#10b981" };
  if (score >= 55) return { name: "B-TIER", class: "tier-b", glow: "#a855f7" };
  if (score >= 40) return { name: "C-TIER", class: "tier-c", glow: "#f59e0b" };
  return { name: "D-TIER", class: "tier-d", glow: "#ef4444" };
}

function analyzeResume(text) {
  const candidateSkills = detectSkills(text);
  const candidatePrograms = detectPrograms(text);

  const allRoleResults = [];

  for (const [role, roleData] of Object.entries(JOB_ROLES)) {
    const analysis = calculateRoleScore(candidateSkills, candidatePrograms, roleData);
    allRoleResults.push({
      role,
      category: roleData.category,
      description: roleData.description,
      programs: roleData.programs,
      ...analysis
    });
  }

  allRoleResults.sort((a, b) => b.score - a.score);

  return {
    candidateSkills,
    candidatePrograms,
    topRoles: allRoleResults.slice(0, 5),
    allRoles: allRoleResults,
    textLength: text.length,
    wordCount: text.trim().split(/\s+/).length
  };
}

// =========================================================
// PDF & DOCX EXTRACTORS
// =========================================================
async function extractTextFromPDF(arrayBuffer) {
  if (!window.pdfjsLib) {
    throw new Error("PDF.js engine is still loading. Please try again.");
  }
  const loadingTask = window.pdfjsLib.getDocument({ data: arrayBuffer });
  const pdf = await loadingTask.promise;
  let fullText = "";

  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const content = await page.getTextContent();
    const strings = content.items.map(item => item.str);
    fullText += strings.join(" ") + "\n";
  }

  return fullText;
}

async function extractTextFromDOCX(arrayBuffer) {
  if (!window.mammoth) {
    throw new Error("DOCX parser not available. Please paste text or use PDF/TXT.");
  }
  const result = await window.mammoth.extractRawText({ arrayBuffer: arrayBuffer });
  return result.value;
}

// Export global API
window.NexusAnalyzer = {
  JOB_ROLES,
  ALIASES,
  PROGRAM_ALIASES,
  SAMPLE_RESUME_TEXT,
  audio,
  normalizeText,
  detectSkills,
  detectPrograms,
  calculateRoleScore,
  analyzeResume,
  extractTextFromPDF,
  extractTextFromDOCX
};
