"""
Helper functions for seeding procedural memory.
Provides simple interface for creating procedures without needing the full agent system.
"""

from datetime import datetime
from typing import List
from database_manager import MongoDBManager

# Initialize database manager
db_manager = MongoDBManager()

def create_procedure(procedure_name: str, steps: List[str], description: str):
    """
    Create a simple procedural memory entry.
    
    Args:
        procedure_name: Name/identifier for the procedure
        steps: List of step descriptions
        description: Overall description of what the procedure does
    """
    procedure_doc = {
        "procedure_name": procedure_name,
        "description": description,
        "steps": steps,
        "actions": [{"step": i+1, "action": step} for i, step in enumerate(steps)],
        "procedure_type": "standard",
        "success_history": [],
        "execution_count": 0,
        "confidence_score": 0.8,  # Default confidence for standard procedures
        "success_rate": 0.0,
        "version": 1,
        "created_at": datetime.utcnow(),
        "last_updated": datetime.utcnow()
    }
    
    try:
        result = db_manager.db.procedural_memories.insert_one(procedure_doc)
        return result.inserted_id
    except Exception as e:
        print(f"  ✗ Error creating procedure '{procedure_name}': {e}")
        raise e

def get_all_procedures():
    """Retrieve all procedural memories."""
    return list(db_manager.db.procedural_memories.find())

def delete_all_procedures():
    """Delete all procedural memories (use with caution!)."""
    result = db_manager.db.procedural_memories.delete_many({})
    return result.deleted_count