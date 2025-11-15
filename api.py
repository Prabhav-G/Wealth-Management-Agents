
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Lazy imports to allow server to start without MongoDB configured
# These will only be imported when the endpoints that need them are called

app = FastAPI(title="Multi-Agent Wealth Advisory System API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for running synchronous analysis
executor = ThreadPoolExecutor(max_workers=2)

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Serve static files (HTML, CSS, JS) - mount this AFTER the root route
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_path = os.path.join(static_dir, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Error: static/index.html not found</h1>", status_code=404)

# --- Semantic Memory Endpoints ---
class SemanticMemoryCreate(BaseModel):
    client_id: str
    memory_type: str
    data: dict
    description: Optional[str] = None

@app.post("/semantic/create")
async def create_semantic(memory_data: SemanticMemoryCreate):
    try:
        import semantic_memory
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
        import semantic_memory
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
        import semantic_memory
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
        import semantic_memory
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
        from episodic_memory import episodic_memory
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
        from episodic_memory import episodic_memory
        memories = episodic_memory.retrieve_memories(
            client_id=client_id, query=query, top_k=top_k
        )
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Procedural Memory Endpoints ---
# Lazy import - only include router when needed
def get_procedural_router():
    from procedural_memory import procedural_memory
    return procedural_memory.router

# Note: This will still require MongoDB when accessed, but allows server to start
try:
    from procedural_memory import procedural_memory
    app.include_router(procedural_memory.router, prefix="/procedural")
except (ValueError, ImportError) as e:
    # If MongoDB isn't configured, create a placeholder endpoint
    @app.get("/procedural/")
    async def procedural_not_available():
        raise HTTPException(status_code=503, detail="MongoDB not configured. Please set MONGODB_URL in .env file")

# --- Financial Analysis Endpoint ---
class ClientData(BaseModel):
    profile: Dict[str, Any]
    portfolio: Dict[str, Any]
    tax_info: Optional[Dict[str, Any]] = {}
    goals: List[Dict[str, Any]] = []

def run_analysis(client_data_dict: Dict):
    """Run analysis in a separate thread"""
    # Import here to avoid requiring MongoDB at server startup
    from orchestrator import FinancialAdvisoryOrchestrator
    orchestrator = FinancialAdvisoryOrchestrator()
    results = orchestrator.comprehensive_analysis(client_data_dict)
    report = orchestrator.generate_report(results)
    return results, report

@app.post("/api/analyze")
async def analyze_financial_strategy(client_data: ClientData):
    """Run comprehensive financial analysis based on client data"""
    try:
        # Run the analysis in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        results, report = await loop.run_in_executor(
            executor, 
            run_analysis, 
            client_data.dict()
        )
        return {
            "status": "success",
            "results": results,
            "report": report
        }
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}\n{traceback.format_exc()}")
