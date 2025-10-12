import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

from bson import ObjectId
from pymongo import MongoClient

from database_manager import MongoDBManager

mongo_db = MongoDBManager().db


def _get_clients():
    """Lazy initialization of AI clients."""
    from llama_client import get_voyage_client, get_fireworks_client
    import config
    return get_voyage_client(), get_fireworks_client(), config


def detect_relationships(client_id, memory_type, data):
    """
    Detect relationships between memories.
    This is a placeholder. In a real implementation, this function would
    query the database for related memories and use a language model
    to identify relationships.
    """
    return []


def create_semantic_memory(client_id: str, memory_type: str, data: Dict[str, Any]):
    """
    Create a new semantic memory for a client.
    """
    print(f"  - Creating semantic memory for: {client_id} -> {memory_type}")

    # Get clients lazily
    voyage_client, fireworks_client, config = _get_clients()

    # 1. Generate a summary using Fireworks AI
    prompt = f"""
    Based on the following data for a client's {memory_type}, generate a concise
    and structured summary. The summary should be a JSON object containing the
    most important, factual information.

    Data:
    {json.dumps(data, indent=2)}

    Respond with ONLY the JSON summary.
    """

    try:
        response = fireworks_client.chat.completions.create(
            model=config.FIREWORKS_MODEL,  # Use the model from the central config
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=1000
        )
        summary_json = json.loads(response.choices[0].message.content)

    except Exception as e:
        # Provides a more informative error message upon failure
        print(f"  ✗ Error creating semantic memory: {e}")
        raise

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
    return str(result.inserted_id)


def get_semantic_memory(client_id: str, memory_type: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a semantic memory for a client.
    """
    return mongo_db.semantic_memories.find_one({
        "client_id": client_id,
        "memory_type": memory_type,
        "is_active": True
    })


def retrieve_semantic_memories(client_id: str, memory_type: str = None) -> List[Dict[str, Any]]:
    """
    Retrieve all semantic memories for a client.
    
    Args:
        client_id: Client identifier
        memory_type: Optional filter by memory type
    
    Returns:
        List of semantic memories
    """
    query = {"client_id": client_id, "is_active": True}
    if memory_type:
        query["memory_type"] = memory_type
    
    return list(mongo_db.semantic_memories.find(query))


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
    voyage_client, _, _ = _get_clients()
    
    query_embedding = voyage_client.embed(
        texts=[query],
        model="voyage-large-2-instruct"
    ).embeddings[0]

    results = mongo_db.semantic_memories.aggregate([
        {
            "$vectorSearch": {
                "index": "semantic_vector_index", # Make sure this index exists
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