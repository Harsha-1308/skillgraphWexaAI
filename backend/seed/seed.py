#!/usr/bin/env python3
"""
SkillGraph Seed Script
======================
Loads realistic synthetic data into CognoDB using MERGE to be idempotent.
Run: python seed/seed.py
Requires COGNODB_URI, COGNODB_USERNAME, COGNODB_PASSWORD environment variables.
"""
import logging
import os
import sys
from pathlib import Path

# Allow running from project root or seed/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_driver():
    uri = os.environ.get("COGNODB_URI")
    username = os.environ.get("COGNODB_USERNAME", "cognodb")
    password = os.environ.get("COGNODB_PASSWORD")
    if not uri or not password:
        logger.error("COGNODB_URI and COGNODB_PASSWORD environment variables are required.")
        sys.exit(1)
    return GraphDatabase.driver(uri, auth=(username, password))


# ─────────────────────────────────────────────
# SEED DATA
# ─────────────────────────────────────────────

LOCATIONS = [
    {"id": "loc-san-francisco", "city": "San Francisco", "country": "USA"},
    {"id": "loc-new-york", "city": "New York", "country": "USA"},
    {"id": "loc-seattle", "city": "Seattle", "country": "USA"},
    {"id": "loc-austin", "city": "Austin", "country": "USA"},
    {"id": "loc-boston", "city": "Boston", "country": "USA"},
    {"id": "loc-london", "city": "London", "country": "UK"},
    {"id": "loc-berlin", "city": "Berlin", "country": "Germany"},
    {"id": "loc-toronto", "city": "Toronto", "country": "Canada"},
    {"id": "loc-remote", "city": "Remote", "country": "Worldwide"},
    {"id": "loc-bangalore", "city": "Bangalore", "country": "India"},
]

SKILLS = [
    # Programming Languages
    {"id": "skill-python", "name": "Python", "category": "Programming", "level": "advanced"},
    {"id": "skill-java", "name": "Java", "category": "Programming", "level": "advanced"},
    {"id": "skill-javascript", "name": "JavaScript", "category": "Programming", "level": "advanced"},
    {"id": "skill-typescript", "name": "TypeScript", "category": "Programming", "level": "intermediate"},
    {"id": "skill-go", "name": "Go", "category": "Programming", "level": "intermediate"},
    # Frontend
    {"id": "skill-react", "name": "React", "category": "Frontend", "level": "intermediate"},
    {"id": "skill-nodejs", "name": "Node.js", "category": "Backend", "level": "intermediate"},
    {"id": "skill-graphql", "name": "GraphQL", "category": "Backend", "level": "intermediate"},
    {"id": "skill-rest-apis", "name": "REST APIs", "category": "Backend", "level": "intermediate"},
    # Python Web Frameworks
    {"id": "skill-fastapi", "name": "FastAPI", "category": "Backend", "level": "intermediate"},
    {"id": "skill-flask", "name": "Flask", "category": "Backend", "level": "beginner"},
    {"id": "skill-django", "name": "Django", "category": "Backend", "level": "intermediate"},
    {"id": "skill-springboot", "name": "Spring Boot", "category": "Backend", "level": "intermediate"},
    # Databases
    {"id": "skill-sql", "name": "SQL", "category": "Database", "level": "intermediate"},
    {"id": "skill-postgresql", "name": "PostgreSQL", "category": "Database", "level": "intermediate"},
    {"id": "skill-mongodb", "name": "MongoDB", "category": "Database", "level": "intermediate"},
    {"id": "skill-neo4j", "name": "Neo4j", "category": "Database", "level": "intermediate"},
    {"id": "skill-redis", "name": "Redis", "category": "Database", "level": "beginner"},
    # ML/AI
    {"id": "skill-ml", "name": "Machine Learning", "category": "AI/ML", "level": "advanced"},
    {"id": "skill-deep-learning", "name": "Deep Learning", "category": "AI/ML", "level": "advanced"},
    {"id": "skill-nlp", "name": "NLP", "category": "AI/ML", "level": "advanced"},
    {"id": "skill-gen-ai", "name": "Generative AI", "category": "AI/ML", "level": "advanced"},
    {"id": "skill-rag", "name": "RAG", "category": "AI/ML", "level": "intermediate"},
    {"id": "skill-llms", "name": "LLMs", "category": "AI/ML", "level": "intermediate"},
    {"id": "skill-pytorch", "name": "PyTorch", "category": "AI/ML", "level": "intermediate"},
    {"id": "skill-tensorflow", "name": "TensorFlow", "category": "AI/ML", "level": "intermediate"},
    {"id": "skill-computer-vision", "name": "Computer Vision", "category": "AI/ML", "level": "advanced"},
    # Cloud & DevOps
    {"id": "skill-docker", "name": "Docker", "category": "DevOps", "level": "intermediate"},
    {"id": "skill-kubernetes", "name": "Kubernetes", "category": "DevOps", "level": "intermediate"},
    {"id": "skill-aws", "name": "AWS", "category": "Cloud", "level": "intermediate"},
    {"id": "skill-azure", "name": "Azure", "category": "Cloud", "level": "intermediate"},
    {"id": "skill-cicd", "name": "CI/CD", "category": "DevOps", "level": "intermediate"},
    {"id": "skill-kafka", "name": "Kafka", "category": "Data Engineering", "level": "intermediate"},
    # General
    {"id": "skill-git", "name": "Git", "category": "Tools", "level": "beginner"},
    {"id": "skill-system-design", "name": "System Design", "category": "Architecture", "level": "advanced"},
    {"id": "skill-linux", "name": "Linux", "category": "Tools", "level": "intermediate"},
    {"id": "skill-data-structures", "name": "Data Structures", "category": "CS Fundamentals", "level": "intermediate"},
    {"id": "skill-algorithms", "name": "Algorithms", "category": "CS Fundamentals", "level": "intermediate"},
]

# (from, to, strength 0-1)
SKILL_RELATIONS = [
    # Python ecosystem
    ("skill-python", "skill-fastapi", 0.9),
    ("skill-python", "skill-flask", 0.85),
    ("skill-python", "skill-django", 0.85),
    ("skill-python", "skill-ml", 0.8),
    ("skill-python", "skill-data-structures", 0.7),
    ("skill-fastapi", "skill-rest-apis", 0.9),
    ("skill-flask", "skill-rest-apis", 0.85),
    ("skill-django", "skill-postgresql", 0.75),
    # JavaScript ecosystem
    ("skill-javascript", "skill-typescript", 0.95),
    ("skill-javascript", "skill-react", 0.9),
    ("skill-javascript", "skill-nodejs", 0.85),
    ("skill-typescript", "skill-react", 0.9),
    ("skill-typescript", "skill-nodejs", 0.8),
    ("skill-react", "skill-graphql", 0.7),
    ("skill-nodejs", "skill-rest-apis", 0.8),
    ("skill-nodejs", "skill-graphql", 0.75),
    # Java ecosystem
    ("skill-java", "skill-springboot", 0.9),
    ("skill-java", "skill-data-structures", 0.8),
    ("skill-java", "skill-algorithms", 0.8),
    ("skill-springboot", "skill-rest-apis", 0.85),
    # AI/ML hierarchy
    ("skill-ml", "skill-deep-learning", 0.85),
    ("skill-ml", "skill-pytorch", 0.8),
    ("skill-ml", "skill-tensorflow", 0.8),
    ("skill-deep-learning", "skill-computer-vision", 0.85),
    ("skill-deep-learning", "skill-nlp", 0.8),
    ("skill-deep-learning", "skill-pytorch", 0.9),
    ("skill-nlp", "skill-gen-ai", 0.9),
    ("skill-nlp", "skill-llms", 0.85),
    ("skill-gen-ai", "skill-rag", 0.9),
    ("skill-gen-ai", "skill-llms", 0.95),
    ("skill-rag", "skill-llms", 0.9),
    # Cloud / DevOps
    ("skill-docker", "skill-kubernetes", 0.9),
    ("skill-docker", "skill-cicd", 0.8),
    ("skill-kubernetes", "skill-aws", 0.75),
    ("skill-aws", "skill-docker", 0.8),
    ("skill-aws", "skill-cicd", 0.75),
    ("skill-cicd", "skill-linux", 0.7),
    ("skill-cicd", "skill-git", 0.85),
    # Databases
    ("skill-sql", "skill-postgresql", 0.95),
    ("skill-postgresql", "skill-mongodb", 0.6),
    ("skill-mongodb", "skill-redis", 0.5),
    ("skill-neo4j", "skill-sql", 0.5),
    # Kafka / data engineering
    ("skill-kafka", "skill-aws", 0.6),
    ("skill-kafka", "skill-docker", 0.6),
    # CS Fundamentals
    ("skill-data-structures", "skill-algorithms", 0.95),
    ("skill-algorithms", "skill-system-design", 0.8),
    ("skill-system-design", "skill-aws", 0.7),
]

ROLES = [
    {"id": "role-ml-engineer", "name": "Machine Learning Engineer"},
    {"id": "role-backend-engineer", "name": "Backend Engineer"},
    {"id": "role-fullstack-engineer", "name": "Full-Stack Engineer"},
    {"id": "role-data-engineer", "name": "Data Engineer"},
    {"id": "role-devops-engineer", "name": "DevOps Engineer"},
    {"id": "role-ai-researcher", "name": "AI Researcher"},
    {"id": "role-frontend-engineer", "name": "Frontend Engineer"},
    {"id": "role-software-architect", "name": "Software Architect"},
    {"id": "role-platform-engineer", "name": "Platform Engineer"},
    {"id": "role-data-scientist", "name": "Data Scientist"},
]

COMPANIES = [
    {"id": "co-nexus", "name": "Nexus AI", "industry": "Artificial Intelligence",
     "description": "Building next-generation AI infrastructure and foundation models.",
     "location": "San Francisco, CA", "loc_id": "loc-san-francisco"},
    {"id": "co-dataflow", "name": "DataFlow Systems", "industry": "Data Engineering",
     "description": "Real-time data pipelines and streaming analytics at scale.",
     "location": "Seattle, WA", "loc_id": "loc-seattle"},
    {"id": "co-cloudedge", "name": "CloudEdge", "industry": "Cloud Computing",
     "description": "Cloud-native platform engineering and Kubernetes-first infrastructure.",
     "location": "Austin, TX", "loc_id": "loc-austin"},
    {"id": "co-graphmind", "name": "GraphMind", "industry": "Graph Analytics",
     "description": "Graph database solutions for enterprise knowledge management.",
     "location": "Boston, MA", "loc_id": "loc-boston"},
    {"id": "co-visionix", "name": "Visionix", "industry": "Computer Vision",
     "description": "Computer vision and video AI for retail and manufacturing.",
     "location": "San Francisco, CA", "loc_id": "loc-san-francisco"},
    {"id": "co-llmstack", "name": "LLMStack", "industry": "Generative AI",
     "description": "Developer tools for building and deploying LLM-powered applications.",
     "location": "New York, NY", "loc_id": "loc-new-york"},
    {"id": "co-finbridge", "name": "FinBridge", "industry": "FinTech",
     "description": "Real-time payments infrastructure connecting banks and payment processors.",
     "location": "New York, NY", "loc_id": "loc-new-york"},
    {"id": "co-healthgraph", "name": "HealthGraph", "industry": "HealthTech",
     "description": "Knowledge graph platform for clinical decision support.",
     "location": "Boston, MA", "loc_id": "loc-boston"},
    {"id": "co-devhub", "name": "DevHub", "industry": "Developer Tools",
     "description": "CI/CD and developer platform for engineering teams.",
     "location": "Remote", "loc_id": "loc-remote"},
    {"id": "co-ecomflow", "name": "EcomFlow", "industry": "E-Commerce",
     "description": "AI-powered personalisation and recommendation engine for e-commerce.",
     "location": "London, UK", "loc_id": "loc-london"},
]

JOBS = [
    {
        "id": "job-nexus-mle", "title": "Senior ML Engineer",
        "description": "Design and train large-scale ML models for our AI platform. Work with Python, PyTorch, and distributed training infrastructure.",
        "experience_required": 4, "location": "San Francisco, CA",
        "employment_type": "full-time", "salary_min": 160000, "salary_max": 220000,
        "company_id": "co-nexus", "role_id": "role-ml-engineer",
        "required_skills": [
            {"skill_id": "skill-python", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-ml", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-deep-learning", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-pytorch", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-docker", "minimum_level": "beginner", "importance": "medium"},
            {"skill_id": "skill-aws", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-nexus-research", "title": "AI Research Scientist",
        "description": "Conduct research on foundation models, self-supervised learning, and multimodal AI. Publish to top conferences.",
        "experience_required": 3, "location": "San Francisco, CA",
        "employment_type": "full-time", "salary_min": 180000, "salary_max": 260000,
        "company_id": "co-nexus", "role_id": "role-ai-researcher",
        "required_skills": [
            {"skill_id": "skill-ml", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-deep-learning", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-python", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-pytorch", "minimum_level": "advanced", "importance": "high"},
            {"skill_id": "skill-nlp", "minimum_level": "intermediate", "importance": "high"},
        ]
    },
    {
        "id": "job-dataflow-backend", "title": "Backend Engineer — Streaming",
        "description": "Build and maintain real-time data pipelines using Kafka and Python. Design APIs with FastAPI.",
        "experience_required": 3, "location": "Seattle, WA",
        "employment_type": "full-time", "salary_min": 130000, "salary_max": 175000,
        "company_id": "co-dataflow", "role_id": "role-backend-engineer",
        "required_skills": [
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-kafka", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-fastapi", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-postgresql", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-docker", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-dataflow-data-eng", "title": "Data Engineer",
        "description": "Design and implement ELT pipelines, data models, and warehouse integrations.",
        "experience_required": 2, "location": "Seattle, WA",
        "employment_type": "full-time", "salary_min": 115000, "salary_max": 155000,
        "company_id": "co-dataflow", "role_id": "role-data-engineer",
        "required_skills": [
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-sql", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-kafka", "minimum_level": "beginner", "importance": "high"},
            {"skill_id": "skill-aws", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-cloudedge-platform", "title": "Platform Engineer",
        "description": "Manage Kubernetes clusters, design CI/CD pipelines, and build developer experience tools.",
        "experience_required": 4, "location": "Austin, TX",
        "employment_type": "full-time", "salary_min": 140000, "salary_max": 190000,
        "company_id": "co-cloudedge", "role_id": "role-platform-engineer",
        "required_skills": [
            {"skill_id": "skill-kubernetes", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-docker", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-aws", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-cicd", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-linux", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-go", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-cloudedge-devops", "title": "DevOps Engineer",
        "description": "Build and maintain CI/CD systems, monitoring infrastructure, and cloud automation.",
        "experience_required": 2, "location": "Austin, TX",
        "employment_type": "full-time", "salary_min": 110000, "salary_max": 150000,
        "company_id": "co-cloudedge", "role_id": "role-devops-engineer",
        "required_skills": [
            {"skill_id": "skill-docker", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-cicd", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-linux", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-aws", "minimum_level": "beginner", "importance": "high"},
            {"skill_id": "skill-kubernetes", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-graphmind-backend", "title": "Graph Backend Engineer",
        "description": "Design graph schemas and implement APIs for enterprise knowledge graph products using Neo4j and Cypher.",
        "experience_required": 3, "location": "Boston, MA",
        "employment_type": "full-time", "salary_min": 125000, "salary_max": 170000,
        "company_id": "co-graphmind", "role_id": "role-backend-engineer",
        "required_skills": [
            {"skill_id": "skill-neo4j", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-fastapi", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-system-design", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-rest-apis", "minimum_level": "intermediate", "importance": "high"},
        ]
    },
    {
        "id": "job-visionix-cv", "title": "Computer Vision Engineer",
        "description": "Build real-time video inference pipelines and deploy vision models for retail analytics.",
        "experience_required": 3, "location": "San Francisco, CA",
        "employment_type": "full-time", "salary_min": 150000, "salary_max": 200000,
        "company_id": "co-visionix", "role_id": "role-ml-engineer",
        "required_skills": [
            {"skill_id": "skill-computer-vision", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-deep-learning", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-python", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-pytorch", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-docker", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-llmstack-backend", "title": "LLM Backend Engineer",
        "description": "Build APIs and orchestration layers for LLM-powered applications. Work with RAG pipelines and vector databases.",
        "experience_required": 2, "location": "New York, NY",
        "employment_type": "full-time", "salary_min": 140000, "salary_max": 190000,
        "company_id": "co-llmstack", "role_id": "role-backend-engineer",
        "required_skills": [
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-llms", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-rag", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-fastapi", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-gen-ai", "minimum_level": "beginner", "importance": "high"},
        ]
    },
    {
        "id": "job-llmstack-fullstack", "title": "Full-Stack AI Product Engineer",
        "description": "Build and ship full-stack features for our developer-facing LLM playground and API console.",
        "experience_required": 3, "location": "New York, NY",
        "employment_type": "full-time", "salary_min": 130000, "salary_max": 175000,
        "company_id": "co-llmstack", "role_id": "role-fullstack-engineer",
        "required_skills": [
            {"skill_id": "skill-typescript", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-react", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-fastapi", "minimum_level": "beginner", "importance": "medium"},
            {"skill_id": "skill-rest-apis", "minimum_level": "intermediate", "importance": "high"},
        ]
    },
    {
        "id": "job-finbridge-backend", "title": "Senior Backend Engineer — Payments",
        "description": "Build high-throughput payment processing APIs with strict SLAs. Java/Spring Boot stack.",
        "experience_required": 5, "location": "New York, NY",
        "employment_type": "full-time", "salary_min": 160000, "salary_max": 220000,
        "company_id": "co-finbridge", "role_id": "role-backend-engineer",
        "required_skills": [
            {"skill_id": "skill-java", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-springboot", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-postgresql", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-kafka", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-system-design", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-redis", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-healthgraph-data-sci", "title": "Data Scientist — Clinical AI",
        "description": "Apply ML and graph analytics to clinical data for decision support and drug discovery.",
        "experience_required": 3, "location": "Boston, MA",
        "employment_type": "full-time", "salary_min": 130000, "salary_max": 175000,
        "company_id": "co-healthgraph", "role_id": "role-data-scientist",
        "required_skills": [
            {"skill_id": "skill-python", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-ml", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-sql", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-pytorch", "minimum_level": "intermediate", "importance": "medium"},
            {"skill_id": "skill-neo4j", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-devhub-platform", "title": "Developer Platform Engineer",
        "description": "Build and maintain our CI/CD platform. Improve DX for hundreds of engineering teams.",
        "experience_required": 3, "location": "Remote",
        "employment_type": "full-time", "salary_min": 120000, "salary_max": 165000,
        "company_id": "co-devhub", "role_id": "role-devops-engineer",
        "required_skills": [
            {"skill_id": "skill-cicd", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-docker", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-kubernetes", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-go", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-aws", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-linux", "minimum_level": "intermediate", "importance": "medium"},
        ]
    },
    {
        "id": "job-ecomflow-ml", "title": "ML Engineer — Recommendations",
        "description": "Build and improve recommendation systems using ML and graph-based collaborative filtering.",
        "experience_required": 3, "location": "London, UK",
        "employment_type": "full-time", "salary_min": 90000, "salary_max": 130000,
        "company_id": "co-ecomflow", "role_id": "role-ml-engineer",
        "required_skills": [
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-ml", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-sql", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-neo4j", "minimum_level": "beginner", "importance": "medium"},
            {"skill_id": "skill-aws", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-ecomflow-fullstack", "title": "Full-Stack Engineer — Storefront",
        "description": "Build customer-facing React storefronts with a Node.js/GraphQL backend.",
        "experience_required": 2, "location": "London, UK",
        "employment_type": "full-time", "salary_min": 75000, "salary_max": 105000,
        "company_id": "co-ecomflow", "role_id": "role-fullstack-engineer",
        "required_skills": [
            {"skill_id": "skill-typescript", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-react", "minimum_level": "intermediate", "importance": "critical"},
            {"skill_id": "skill-nodejs", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-graphql", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-postgresql", "minimum_level": "beginner", "importance": "medium"},
        ]
    },
    {
        "id": "job-graphmind-architect", "title": "Software Architect",
        "description": "Define technical direction and review system-level designs for scalable graph analytics products.",
        "experience_required": 7, "location": "Boston, MA",
        "employment_type": "full-time", "salary_min": 180000, "salary_max": 240000,
        "company_id": "co-graphmind", "role_id": "role-software-architect",
        "required_skills": [
            {"skill_id": "skill-system-design", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-neo4j", "minimum_level": "advanced", "importance": "critical"},
            {"skill_id": "skill-python", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-java", "minimum_level": "intermediate", "importance": "medium"},
            {"skill_id": "skill-kafka", "minimum_level": "intermediate", "importance": "high"},
            {"skill_id": "skill-kubernetes", "minimum_level": "intermediate", "importance": "medium"},
        ]
    },
]

CANDIDATES = [
    {
        "id": "cand-alex", "name": "Alex Chen",
        "email": "alex.chen@example.com", "experience_years": 5,
        "location": "San Francisco, CA", "bio": "ML engineer with 5 years in deep learning and computer vision. Passionate about building scalable model training infrastructure.",
        "skills": [
            {"skill_id": "skill-python", "level": "expert", "years": 5.0},
            {"skill_id": "skill-ml", "level": "advanced", "years": 4.0},
            {"skill_id": "skill-deep-learning", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-pytorch", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-computer-vision", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-docker", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-git", "level": "advanced", "years": 5.0},
        ]
    },
    {
        "id": "cand-sarah", "name": "Sarah Miller",
        "email": "sarah.miller@example.com", "experience_years": 3,
        "location": "New York, NY", "bio": "Full-stack developer specialising in TypeScript and React with a growing interest in AI-powered product features.",
        "skills": [
            {"skill_id": "skill-typescript", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-react", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-javascript", "level": "expert", "years": 4.0},
            {"skill_id": "skill-nodejs", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-graphql", "level": "intermediate", "years": 1.5},
            {"skill_id": "skill-python", "level": "beginner", "years": 0.5},
            {"skill_id": "skill-git", "level": "advanced", "years": 4.0},
        ]
    },
    {
        "id": "cand-james", "name": "James Okafor",
        "email": "james.okafor@example.com", "experience_years": 7,
        "location": "Austin, TX", "bio": "Platform engineer and DevOps specialist. 7 years running production Kubernetes clusters and building CI/CD for large engineering orgs.",
        "skills": [
            {"skill_id": "skill-kubernetes", "level": "expert", "years": 5.0},
            {"skill_id": "skill-docker", "level": "expert", "years": 6.0},
            {"skill_id": "skill-aws", "level": "advanced", "years": 5.0},
            {"skill_id": "skill-cicd", "level": "advanced", "years": 5.0},
            {"skill_id": "skill-linux", "level": "advanced", "years": 7.0},
            {"skill_id": "skill-go", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-python", "level": "intermediate", "years": 3.0},
            {"skill_id": "skill-git", "level": "advanced", "years": 7.0},
        ]
    },
    {
        "id": "cand-priya", "name": "Priya Sharma",
        "email": "priya.sharma@example.com", "experience_years": 4,
        "location": "Bangalore, India", "bio": "Backend engineer with deep expertise in Python and data engineering. Building real-time pipelines with Kafka and FastAPI.",
        "skills": [
            {"skill_id": "skill-python", "level": "advanced", "years": 4.0},
            {"skill_id": "skill-fastapi", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-kafka", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-postgresql", "level": "intermediate", "years": 3.0},
            {"skill_id": "skill-sql", "level": "advanced", "years": 4.0},
            {"skill_id": "skill-docker", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-redis", "level": "beginner", "years": 1.0},
            {"skill_id": "skill-git", "level": "advanced", "years": 4.0},
        ]
    },
    {
        "id": "cand-david", "name": "David Kim",
        "email": "david.kim@example.com", "experience_years": 6,
        "location": "Seattle, WA", "bio": "Java backend engineer transitioning into Generative AI. Strong foundation in distributed systems and Spring Boot.",
        "skills": [
            {"skill_id": "skill-java", "level": "expert", "years": 6.0},
            {"skill_id": "skill-springboot", "level": "advanced", "years": 5.0},
            {"skill_id": "skill-postgresql", "level": "advanced", "years": 4.0},
            {"skill_id": "skill-kafka", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-system-design", "level": "advanced", "years": 5.0},
            {"skill_id": "skill-docker", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-redis", "level": "beginner", "years": 1.0},
            {"skill_id": "skill-git", "level": "advanced", "years": 6.0},
        ]
    },
    {
        "id": "cand-emma", "name": "Emma Wilson",
        "email": "emma.wilson@example.com", "experience_years": 2,
        "location": "London, UK", "bio": "Junior NLP engineer, recently graduated, working on LLM fine-tuning and RAG systems.",
        "skills": [
            {"skill_id": "skill-python", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-nlp", "level": "intermediate", "years": 1.5},
            {"skill_id": "skill-llms", "level": "intermediate", "years": 1.0},
            {"skill_id": "skill-rag", "level": "beginner", "years": 0.5},
            {"skill_id": "skill-pytorch", "level": "beginner", "years": 1.0},
            {"skill_id": "skill-git", "level": "intermediate", "years": 2.0},
        ]
    },
    {
        "id": "cand-marcus", "name": "Marcus Johnson",
        "email": "marcus.johnson@example.com", "experience_years": 8,
        "location": "Boston, MA", "bio": "Software architect and graph database enthusiast. Built several large-scale knowledge graph systems.",
        "skills": [
            {"skill_id": "skill-neo4j", "level": "expert", "years": 5.0},
            {"skill_id": "skill-python", "level": "advanced", "years": 7.0},
            {"skill_id": "skill-java", "level": "advanced", "years": 6.0},
            {"skill_id": "skill-system-design", "level": "expert", "years": 7.0},
            {"skill_id": "skill-kafka", "level": "advanced", "years": 4.0},
            {"skill_id": "skill-kubernetes", "level": "intermediate", "years": 3.0},
            {"skill_id": "skill-fastapi", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-sql", "level": "advanced", "years": 6.0},
        ]
    },
    {
        "id": "cand-luna", "name": "Luna Park",
        "email": "luna.park@example.com", "experience_years": 1,
        "location": "Remote", "bio": "Recent computer science graduate interested in full-stack development. Building personal projects with React and FastAPI.",
        "skills": [
            {"skill_id": "skill-javascript", "level": "intermediate", "years": 1.5},
            {"skill_id": "skill-react", "level": "beginner", "years": 0.5},
            {"skill_id": "skill-python", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-sql", "level": "beginner", "years": 1.0},
            {"skill_id": "skill-git", "level": "intermediate", "years": 1.5},
            {"skill_id": "skill-data-structures", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-algorithms", "level": "intermediate", "years": 2.0},
        ]
    },
    {
        "id": "cand-raj", "name": "Raj Patel",
        "email": "raj.patel@example.com", "experience_years": 5,
        "location": "Toronto, Canada", "bio": "ML engineer specialised in NLP and Generative AI. Building production RAG systems and LLM evaluation pipelines.",
        "skills": [
            {"skill_id": "skill-python", "level": "advanced", "years": 5.0},
            {"skill_id": "skill-nlp", "level": "advanced", "years": 4.0},
            {"skill_id": "skill-gen-ai", "level": "advanced", "years": 2.0},
            {"skill_id": "skill-rag", "level": "advanced", "years": 2.0},
            {"skill_id": "skill-llms", "level": "advanced", "years": 2.0},
            {"skill_id": "skill-pytorch", "level": "intermediate", "years": 3.0},
            {"skill_id": "skill-fastapi", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-docker", "level": "beginner", "years": 1.0},
        ]
    },
    {
        "id": "cand-olivia", "name": "Olivia Brown",
        "email": "olivia.brown@example.com", "experience_years": 3,
        "location": "Berlin, Germany", "bio": "Full-stack engineer with a background in e-commerce. Strong TypeScript, React, and Node.js skills.",
        "skills": [
            {"skill_id": "skill-typescript", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-react", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-nodejs", "level": "advanced", "years": 2.0},
            {"skill_id": "skill-graphql", "level": "intermediate", "years": 1.5},
            {"skill_id": "skill-postgresql", "level": "intermediate", "years": 2.0},
            {"skill_id": "skill-rest-apis", "level": "advanced", "years": 3.0},
            {"skill_id": "skill-docker", "level": "beginner", "years": 0.5},
        ]
    },
]

# ─────────────────────────────────────────────
# SEED FUNCTIONS
# ─────────────────────────────────────────────

def create_constraints(session):
    constraints = [
        "CREATE CONSTRAINT candidate_id IF NOT EXISTS FOR (c:Candidate) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
        "CREATE CONSTRAINT job_id IF NOT EXISTS FOR (j:Job) REQUIRE j.id IS UNIQUE",
        "CREATE CONSTRAINT company_id IF NOT EXISTS FOR (co:Company) REQUIRE co.id IS UNIQUE",
        "CREATE CONSTRAINT role_id IF NOT EXISTS FOR (r:Role) REQUIRE r.id IS UNIQUE",
        "CREATE CONSTRAINT location_id IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE",
    ]
    for c in constraints:
        try:
            session.run(c)
        except Exception as e:
            logger.warning("Constraint creation note: %s", e)


def seed_locations(session):
    for loc in LOCATIONS:
        session.run(
            "MERGE (l:Location {id: $id}) "
            "SET l.city = $city, l.country = $country",
            id=loc["id"], city=loc["city"], country=loc["country"]
        )
    logger.info("Seeded %d locations.", len(LOCATIONS))


def seed_skills(session):
    for s in SKILLS:
        session.run(
            "MERGE (s:Skill {id: $id}) "
            "SET s.name = $name, s.category = $category, s.level = $level",
            id=s["id"], name=s["name"], category=s["category"], level=s["level"]
        )
    logger.info("Seeded %d skills.", len(SKILLS))


def seed_skill_relations(session):
    count = 0
    for (from_id, to_id, strength) in SKILL_RELATIONS:
        session.run(
            "MATCH (a:Skill {id: $from_id}), (b:Skill {id: $to_id}) "
            "MERGE (a)-[r:RELATED_TO]->(b) "
            "SET r.strength = $strength",
            from_id=from_id, to_id=to_id, strength=strength
        )
        count += 1
    logger.info("Seeded %d skill relationships.", count)


def seed_roles(session):
    for r in ROLES:
        session.run(
            "MERGE (r:Role {id: $id}) SET r.name = $name",
            id=r["id"], name=r["name"]
        )
    logger.info("Seeded %d roles.", len(ROLES))


def seed_companies(session):
    for co in COMPANIES:
        session.run(
            "MERGE (co:Company {id: $id}) "
            "SET co.name = $name, co.industry = $industry, "
            "co.description = $description, co.location = $location",
            id=co["id"], name=co["name"], industry=co["industry"],
            description=co["description"], location=co["location"]
        )
        session.run(
            "MATCH (co:Company {id: $co_id}), (l:Location {id: $loc_id}) "
            "MERGE (co)-[:LOCATED_IN]->(l)",
            co_id=co["id"], loc_id=co["loc_id"]
        )
    logger.info("Seeded %d companies.", len(COMPANIES))


def seed_jobs(session):
    for job in JOBS:
        session.run(
            "MERGE (j:Job {id: $id}) "
            "SET j.title = $title, j.description = $description, "
            "j.experience_required = $experience_required, j.location = $location, "
            "j.employment_type = $employment_type, "
            "j.salary_min = $salary_min, j.salary_max = $salary_max",
            id=job["id"], title=job["title"], description=job["description"],
            experience_required=job["experience_required"], location=job["location"],
            employment_type=job["employment_type"],
            salary_min=job["salary_min"], salary_max=job["salary_max"]
        )
        # Link to company
        session.run(
            "MATCH (j:Job {id: $job_id}), (co:Company {id: $co_id}) "
            "MERGE (j)-[:AT_COMPANY]->(co)",
            job_id=job["id"], co_id=job["company_id"]
        )
        # Link to role
        session.run(
            "MATCH (j:Job {id: $job_id}), (r:Role {id: $role_id}) "
            "MERGE (j)-[:FOR_ROLE]->(r)",
            job_id=job["id"], role_id=job["role_id"]
        )
        # Link to skills
        for skill_req in job["required_skills"]:
            session.run(
                "MATCH (j:Job {id: $job_id}), (s:Skill {id: $skill_id}) "
                "MERGE (j)-[r:REQUIRES_SKILL]->(s) "
                "SET r.minimum_level = $minimum_level, r.importance = $importance",
                job_id=job["id"], skill_id=skill_req["skill_id"],
                minimum_level=skill_req["minimum_level"], importance=skill_req["importance"]
            )
    logger.info("Seeded %d jobs.", len(JOBS))


def seed_candidates(session):
    for cand in CANDIDATES:
        session.run(
            "MERGE (c:Candidate {id: $id}) "
            "SET c.name = $name, c.email = $email, "
            "c.experience_years = $experience_years, "
            "c.location = $location, c.bio = $bio",
            id=cand["id"], name=cand["name"], email=cand["email"],
            experience_years=cand["experience_years"],
            location=cand["location"], bio=cand["bio"]
        )
        for skill in cand["skills"]:
            session.run(
                "MATCH (c:Candidate {id: $cand_id}), (s:Skill {id: $skill_id}) "
                "MERGE (c)-[r:HAS_SKILL]->(s) "
                "SET r.level = $level, r.years = $years",
                cand_id=cand["id"], skill_id=skill["skill_id"],
                level=skill["level"], years=skill["years"]
            )
    logger.info("Seeded %d candidates.", len(CANDIDATES))


def verify_counts(session) -> dict:
    counts = {}
    for label in ["Candidate", "Skill", "Job", "Company", "Role", "Location"]:
        result = session.run(f"MATCH (n:{label}) RETURN count(n) AS cnt")
        counts[label] = result.single()["cnt"]

    rel_result = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt")
    counts["Relationships"] = rel_result.single()["cnt"]
    return counts


def run_smoke_test(session):
    """Run a quick multi-hop traversal to confirm the graph is usable."""
    result = session.run("""
        MATCH (c:Candidate)-[:HAS_SKILL]->(s:Skill)-[:RELATED_TO]->(rs:Skill)<-[:REQUIRES_SKILL]-(j:Job)
        RETURN c.name AS candidate, s.name AS skill, rs.name AS related, j.title AS job
        LIMIT 3
    """)
    rows = result.data()
    if rows:
        logger.info("Smoke test (multi-hop traversal) passed. Sample results:")
        for row in rows:
            logger.info("  %s → %s → %s → %s", row["candidate"], row["skill"], row["related"], row["job"])
    else:
        logger.warning("Smoke test returned no results. Check data and relationships.")


def main():
    logger.info("Connecting to CognoDB...")
    driver = get_driver()
    try:
        driver.verify_connectivity()
        logger.info("Connected successfully.")
    except (ServiceUnavailable, AuthError) as e:
        logger.error("Could not connect to CognoDB: %s", e)
        sys.exit(1)

    with driver.session() as session:
        logger.info("Creating constraints...")
        create_constraints(session)

        logger.info("Seeding locations...")
        seed_locations(session)

        logger.info("Seeding skills...")
        seed_skills(session)

        logger.info("Seeding skill relationships...")
        seed_skill_relations(session)

        logger.info("Seeding roles...")
        seed_roles(session)

        logger.info("Seeding companies...")
        seed_companies(session)

        logger.info("Seeding jobs...")
        seed_jobs(session)

        logger.info("Seeding candidates...")
        seed_candidates(session)

        logger.info("Verifying data...")
        counts = verify_counts(session)

        logger.info("Running smoke test...")
        run_smoke_test(session)

    driver.close()

    print("\n" + "=" * 50)
    print("  Seed completed successfully!")
    print("=" * 50)
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
