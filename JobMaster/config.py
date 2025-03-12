import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o"

# Agent configuration
AGENT_CONFIGS = {
    "job_search": {
        "model": DEFAULT_MODEL,
        "temperature": 0.2,
        "max_tokens": 1000,
    },
    "user_info": {
        "model": DEFAULT_MODEL,
        "temperature": 0.1,
        "max_tokens": 1000,
    },
    "resume": {
        "model": DEFAULT_MODEL,
        "temperature": 0.3,
        "max_tokens": 2000,
    },
    "cover_letter": {
        "model": DEFAULT_MODEL,
        "temperature": 0.4,
        "max_tokens": 1500,
    },
    "interview_prep": {
        "model": DEFAULT_MODEL,
        "temperature": 0.5,
        "max_tokens": 2000,
    },
    "networking": {
        "model": DEFAULT_MODEL,
        "temperature": 0.4,
        "max_tokens": 1000,
    },
}

# Data storage paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")
JOB_DATA_FILE = os.path.join(DATA_DIR, "job_data.json")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True) 