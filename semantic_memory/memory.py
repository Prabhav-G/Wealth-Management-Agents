"""
Semantic Memory System
Handles structured, factual long-term knowledge about clients
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

# CRITICAL: Load environment variables FIRST, before any other imports
from dotenv import load_dotenv

# Find the project root and load the .env file
project_root = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

print("Fireworks Key:", os.getenv("fw_3ZhDcC6YgP5yvHmqYwiagMPx"))
print("Voyage Key:", os.getenv("VOYAGE_API_KEY"))

# Now import other modules
from bson import ObjectId
from pymongo import MongoClient
import voyageai
from fireworks.client import Fireworks

from database_manager import MongoDBManager


# Initialize API keys with validation
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
fw_3ZhDcC6YgP5yvHmqYwiagMPx = os.getenv("fw_3ZhDcC6YgP5yvHmqYwiagMPx")

# Validate API keys
if not VOYAGE_API_KEY:
    raise ValueError("FATAL: VOYAGE_API_KEY not found in .env file. Please check your .env configuration.")
if not fw_3ZhDcC6YgP5yvHmqYwiagMPx:
    raise ValueError("FATAL: fw_3ZhDcC6YgP5yvHmqYwiagMPx not found in .env file. Please check your .env configuration.")

# Debug print (remove in production)
print(f"DEBUG: Fireworks API Key loaded: {fw_3ZhDcC6YgP5yvHmqYwiagMPx[:10]}..." if fw_3ZhDcC6YgP5yvHmqYwiagMPx else "DEBUG: No API key found")

# Initialize clients with explicit API keys
try:
    voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)
    fireworks_client = Fireworks(api_key=fw_3ZhDcC6YgP5yvHmqYwiagMPx)
    mongo_db = MongoDBManager().db
    print("✓ All clients initialized successfully")
except Exception as e:
    print(f"ERROR initializing clients: {e}")
    raise


def detect_relationships(client_id, memory_type, data):
    """
    Detect relationships between memories.
    This is a placeholder for future implementation.
    """
    return []


def create_semantic_memory(client_id: str, memory_type: str, data: Dict[str, Any]):
    """
    Create a new semantic memory for a client.
    """
    print(f"  - Creating semantic memory for: {client_id} -> {memory_type}")

    try:
        # 1. Generate a summary using Fireworks AI
        prompt = f"""
Based on the following data for a client's {memory_type}, generate a concise
and structured summary. The summary should be a JSON object containing the
most important, factual information.

Data:
{json.dumps(data, indent=2)}

Respond with ONLY the JSON summary.
"""

        response = fireworks_client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p1-70b-instruct",  # Updated to a more reliable model
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=1000
        )
        summary_json = json.loads(response.choices[0].message.content)

        # 2. Generate embedding for the summary using Voyage AI
        summary_text = json.dumps(summary_json)
        embedding = voyage_client.embed(
            texts=[summary_text],
            model="voyage-large-2-instruct"
        ).embeddings[0]

        # 3. Detect relationships (placeholder)
        relationships = detect_relationships(client_id, memory_type, data)

        # 4. Store in MongoDB
        memory_doc = {
            "client_id": client_id,
            "memory_type": memory_type,
            "data": data,
            "summary_json": summary_json,
            "summary_text": summary_text,
            "embedding": embedding,
            "relationships": relationships,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "version": 1,
            "is_active": True
        }
        result = mongo_db.semantic_memories.insert_one(memory_doc)
        print(f"  ✓ Successfully stored semantic memory: {memory_type} (ID: {result.inserted_id})")
        
    except Exception as e:
        print(f"  ✗ Error creating semantic memory: {e}")
        raise


def get_semantic_memory(client_id: str, memory_type: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a semantic memory for a client.
    """
    return mongo_db.semantic_memories.find_one({
        "client_id": client_id,
        "memory_type": memory_type,
        "is_active": True
    })


def update_semantic_memory(client_id: str, memory_type: str, new_data: Dict[str, Any]):
    """
    Update an existing semantic memory and archive the old version.
    """
    current_memory = get_semantic_memory(client_id, memory_type)
    if not current_memory:
        # If no memory exists, create a new one
        create_semantic_memory(client_id, memory_type, new_data)
        return

    # Archive the old memory
    archive_doc = current_memory.copy()
    archive_doc["archived_at"] = datetime.utcnow()
    mongo_db.semantic_memories_archive.insert_one(archive_doc)

    # Deactivate the old memory instead of deleting
    mongo_db.semantic_memories.update_one(
        {"_id": current_memory["_id"]},
        {"$set": {"is_active": False}}
    )

    # Create the new, updated memory
    create_semantic_memory(client_id, memory_type, new_data)


def query_semantic_memory(client_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Query semantic memories using vector similarity.
    """
    try:
        query_embedding = voyage_client.embed(
            texts=[query],
            model="voyage-large-2-instruct"
        ).embeddings[0]

        results = mongo_db.semantic_memories.aggregate([
            {
                "$vectorSearch": {
                    "index": "semantic_vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": top_k,
                    "filter": {
                        "client_id": client_id,
                        "is_active": True
                    }
                }
            },
            {
                "$project": {
                    "score": {"$meta": "vectorSearchScore"},
                    "summary_json": 1,
                    "memory_type": 1,
                    "updated_at": 1
                }
            }
        ])
        return list(results)
    except Exception as e:
        print(f"Error querying semantic memory: {e}")
        return []
