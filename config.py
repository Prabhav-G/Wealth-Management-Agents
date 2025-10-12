import os
from dotenv import load_dotenv

# Find the project root and load the .env file
# This makes the environment loading more robust
project_root = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

# Fireworks AI Configuration
FIREWORKS_API_KEY = os.getenv("fw_3ZhDcC6YgP5yvHmqYwiagMPx")
FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
FIREWORKS_MODEL = "accounts/fireworks/models/gpt-oss-20b"

# NOTE: MONGODB_URL and DATABASE_NAME are now managed by the
# singleton MongoDBManager in database_manager.py

# Generation Parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000

# Validate configuration
if not FIREWORKS_API_KEY:
    raise ValueError("FIREWORKS_API_KEY not found. Please set it in .env file")
