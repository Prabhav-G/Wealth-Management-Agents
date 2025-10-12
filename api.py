
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Import memory systems
import semantic_memory
from procedural_memory import procedural_memory
from episodic_memory import episodic_memory

app = FastAPI(title="Multi-Agent Wealth Advisory System API", version="0.1.0")

# --- Semantic Memory Endpoints ---
class SemanticMemoryCreate(BaseModel):
    client_id: str
    memory_type: str
    data: dict
    description: Optional[str] = None

@app.post("/semantic/create")
async def create_semantic(memory_data: SemanticMemoryCreate):
    try:
        semantic_memory.create_semantic_memory(
            client_id=memory_data.client_id,
            memory_type=memory_data.memory_type,
            data=memory_data.data,
            description=memory_data.description,
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/semantic/retrieve")
async def retrieve_semantic(
    client_id: str,
    query: str = None,
    memory_types: List[str] = Query(None),
    include_relationships: bool = True,
):
    try:
        memories = semantic_memory.retrieve_semantic_memories(
            client_id=client_id,
            query=query,
            memory_types=memory_types,
            include_relationships=include_relationships,
        )
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/semantic/update/{memory_id}")
async def update_semantic(memory_id: str, updated_data: dict, update_reason: str):
    try:
        new_memory_id = semantic_memory.update_semantic_memory(
            memory_id=memory_id,
            updated_data=updated_data,
            update_reason=update_reason,
        )
        return {"new_memory_id": new_memory_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/semantic/consistency/{client_id}")
async def check_consistency_endpoint(client_id: str):
    try:
        inconsistencies = semantic_memory.check_consistency(client_id=client_id)
        return {"inconsistencies": inconsistencies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Episodic Memory Endpoints ---
class EpisodicEventCreate(BaseModel):
    client_id: str
    transcript: str
    agent_source: str
    event_type: str
    tags: Optional[List[str]] = None

@app.post("/episodic/add_event")
async def add_episodic_event(event_data: EpisodicEventCreate):
    try:
        event = episodic_memory.add_event(
            client_id=event_data.client_id,
            transcript=event_data.transcript,
            agent_source=event_data.agent_source,
            event_type=event_data.event_type,
            tags=event_data.tags,
        )
        return {"event": event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/episodic/retrieve")
async def retrieve_episodic_memories(
    client_id: str,
    query: str,
    top_k: int = 5,
):
    try:
        memories = episodic_memory.retrieve_memories(
            client_id=client_id, query=query, top_k=top_k
        )
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Procedural Memory Endpoints ---
app.include_router(procedural_memory.router, prefix="/procedural")
