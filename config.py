"""
Configuration file for the Financial Advisory System.
MUST be imported before any other modules that use these settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables FIRST, before anything else
load_dotenv(override=True)

# ===== API Keys =====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FASTINO_API_KEY = os.getenv("FASTINO_API_KEY")
LINKUP_API_KEY = os.getenv("LINKUP_API_KEY")

# Optional: Legacy keys (for backwards compatibility during migration)
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")

# Validate critical keys (warn but don't fail if not set - allows lazy initialization)
if not GEMINI_API_KEY:
    print("⚠ WARNING: GEMINI_API_KEY not found. Set it in .env file for LLM functionality.")

if not FASTINO_API_KEY:
    print("⚠ WARNING: FASTINO_API_KEY not found. Set it in .env file for user profiles.")

if not LINKUP_API_KEY:
    print("⚠ WARNING: LINKUP_API_KEY not found. Set it in .env file for web searching.")

# ===== Gemini AI Settings =====
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1"

# ===== Fastino Settings =====
FASTINO_BASE_URL = os.getenv("FASTINO_BASE_URL", "https://api.fastino.com/v1")

# ===== Linkup Settings =====
LINKUP_BASE_URL = os.getenv("LINKUP_BASE_URL", "https://api.linkup.com/v1")

# ===== Legacy Fireworks AI Settings (deprecated) =====
FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
FIREWORKS_MODEL = "accounts/fireworks/models/llama-v3p1-8b-instruct"

# ===== Legacy Voyage AI Settings (deprecated) =====
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
print(f"  - Gemini API Key: {'✓ Set' if GEMINI_API_KEY else '✗ Missing'}")
print(f"  - Fastino API Key: {'✓ Set' if FASTINO_API_KEY else '✗ Missing'}")
print(f"  - Linkup API Key: {'✓ Set' if LINKUP_API_KEY else '✗ Missing'}")
if FIREWORKS_API_KEY or MONGODB_URL:
    print(f"  - Legacy Fireworks API Key: {'✓ Set' if FIREWORKS_API_KEY else '✗ Missing'}")
    print(f"  - Legacy MongoDB URI: {'✓ Set' if MONGODB_URL else '✗ Missing'}")