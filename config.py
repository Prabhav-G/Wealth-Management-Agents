"""
Configuration file for the Financial Advisory System.
MUST be imported before any other modules that use these settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables FIRST, before anything else
load_dotenv(override=True)

# ===== API Keys =====
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")

# Validate critical keys
if not FIREWORKS_API_KEY:
    raise ValueError("FIREWORKS_API_KEY not found in environment variables. Check your .env file.")

if not MONGODB_URL:
    raise ValueError("MONGODB_URI not found in environment variables. Check your .env file.")

# ===== Fireworks AI Settings =====
FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
FIREWORKS_MODEL = "accounts/fireworks/models/llama-v3p1-8b-instruct"

# ===== Voyage AI Settings =====
VOYAGE_MODEL = "voyage-3"
VOYAGE_INPUT_TYPE = "document"

# ===== LLM Defaults =====
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

# ===== MongoDB Settings =====
DATABASE_NAME = "financial_advisory_system"

# Collections
SEMANTIC_COLLECTION = "semantic_memories"
EPISODIC_COLLECTION = "episodic_memories"
PROCEDURAL_COLLECTION = "procedural_memories"

# Indexes
EPISODIC_VECTOR_INDEX = "episodic_vector_index"

print("✓ Configuration loaded successfully")
print(f"  - Fireworks API Key: {'✓ Set' if FIREWORKS_API_KEY else '✗ Missing'}")
print(f"  - Voyage API Key: {'✓ Set' if VOYAGE_API_KEY else '✗ Missing'}")
print(f"  - MongoDB URI: {'✓ Set' if MONGODB_URL else '✗ Missing'}")