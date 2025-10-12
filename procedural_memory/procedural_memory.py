
from datetime import datetime
from typing import List, Dict
from bson import ObjectId
import json
import os
import voyageai
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from base_agent import BaseFinancialAgent
from llama_client import FireworksAIClient
from database_manager import MongoDBManager

# Initialize clients
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)

class ProceduralMemorySystem(BaseFinancialAgent):
    """
    The Procedural Memory Module captures learned strategies, decision patterns,
    and successful workflows for each client.
    """

    def __init__(self, name: str, role: str, llama_client: FireworksAIClient, db_manager: MongoDBManager):
        super().__init__(name, role, llama_client, db_manager)

    def learn_procedure_from_episodes(self, client_id: str, episode_ids: List[str], procedure_type: str):
        """Extract successful patterns from episodic memories"""

        episodes = self.db_manager.db.episodic_memories.find({
            "memory_id": {"$in": episode_ids},
            "client_id": client_id
        })

        episode_texts = [
            f"Event: {ep['event_summary']}\nOutcome: {ep.get('outcome', 'N/A')}"
            for ep in episodes
        ]
        combined_context = "\n\n".join(episode_texts)

        extraction_prompt = f"""
        Analyze these client interaction episodes and extract a reusable procedure:

        {combined_context}

        Extract:
        1. Trigger conditions (what circumstances led to this action)
        2. Step-by-step actions taken
        3. Agents/roles involved
        4. Success indicators

        Format as a structured procedure.
        """

        procedure_structure_str = self.execute_task(extraction_prompt)
        procedure_structure = json.loads(procedure_structure_str)

        embedding = voyage_client.embed(texts=[procedure_structure['description']], model="voyage-finance-2").embeddings[0]

        procedure_doc = {
            "client_id": client_id,
            "procedure_type": procedure_type,
            **procedure_structure,
            "embedding": embedding,
            "learned_from": episode_ids,
            "success_history": [],
            "execution_count": 0,
            "confidence_score": 0.5,  # Initial confidence
            "created_at": datetime.utcnow()
        }

        self.db_manager.db.procedural_memories.insert_one(procedure_doc)

    def recommend_procedure(self, client_id: str, current_situation: str, top_k: int = 3):
        """Find applicable procedures for current situation"""

        situation_embedding = voyage_client.embed(texts=[current_situation], model="voyage-finance-2").embeddings[0]

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "procedural_vector_index",
                    "path": "embedding",
                    "queryVector": situation_embedding,
                    "numCandidates": 20,
                    "limit": top_k,
                    "filter": {"client_id": client_id}
                }
            },
            {
                "$addFields": {
                    "weighted_score": {
                        "$multiply": [
                            "$score",
                            "$confidence_score",
                            {"$cond": [{"$gt": ["$success_rate", 0]}, "$success_rate", 0.5]}
                        ]
                    }
                }
            },
            {"$sort": {"weighted_score": -1}}
        ]

        recommendations = list(self.db_manager.db.procedural_memories.aggregate(pipeline))

        for rec in recommendations:
            trigger_check_prompt = f"""
                Current situation: {current_situation}

                Procedure triggers: {json.dumps(rec['triggers'])}

                Do the triggers match? Respond with Yes/No and confidence 0-1.
            """
            rec["trigger_match"] = self.execute_task(trigger_check_prompt)

        return recommendations

    def record_procedure_execution(self, procedure_id: str, execution_date: datetime, outcome: str, metrics: dict):
        """Update procedure with execution results"""

        procedure = self.db_manager.db.procedural_memories.find_one({"_id": ObjectId(procedure_id)})

        execution_record = {
            "execution_date": execution_date,
            "outcome": outcome,
            "metrics": metrics
        }

        success_history = procedure.get("success_history", []) + [execution_record]
        success_count = sum(1 for ex in success_history if ex["outcome"] == "success")
        success_rate = success_count / len(success_history)

        execution_count = procedure.get("execution_count", 0) + 1
        confidence_score = min(0.95, 0.5 + (success_rate * 0.45))

        self.db_manager.db.procedural_memories.update_one(
            {"_id": ObjectId(procedure_id)},
            {
                "$push": {"success_history": execution_record},
                "$set": {
                    "success_rate": success_rate,
                    "execution_count": execution_count,
                    "confidence_score": confidence_score,
                    "last_updated": datetime.utcnow()
                }
            }
        )

    def refine_procedure(self, procedure_id: str):
        """Use AI to refine procedure based on execution history"""

        procedure = self.db_manager.db.procedural_memories.find_one({"_id": ObjectId(procedure_id)})

        history_summary = "\n".join([
            f"Date: {ex['execution_date']}, Outcome: {ex['outcome']}, Metrics: {ex['metrics']}"
            for ex in procedure["success_history"][-10:]
        ])

        refinement_prompt = f"""
        Current procedure:
        Name: {procedure['procedure_name']}
        Description: {procedure['description']}
        Actions: {json.dumps(procedure['actions'], indent=2)}

        Recent execution history:
        {history_summary}

        Based on the execution history, suggest refinements to:
        1. Trigger conditions (make them more accurate)
        2. Action steps (improve or reorder)
        3. Success criteria

        Provide refined procedure in the same structure.
        """

        refined_str = self.execute_task(refinement_prompt)
        refined = json.loads(refined_str)

        self.db_manager.db.procedural_memories.update_one(
            {"_id": ObjectId(procedure_id)},
            {
                "$set": {
                    **refined,
                    "version": procedure.get("version", 1) + 1,
                    "last_refined": datetime.utcnow()
                }
            }
        )

# Initialize the procedural memory system
db_manager = MongoDBManager()
llama_client = FireworksAIClient()
procedural_memory_system = ProceduralMemorySystem(
    name="ProceduralMemoryAgent",
    role="Manages and refines learned procedures.",
    llama_client=llama_client,
    db_manager=db_manager
)

router = APIRouter()

class ProcedureExecution(BaseModel):
    execution_date: datetime
    outcome: str
    metrics: Dict

@router.post("/procedural/learn")
async def learn_procedure(
    client_id: str,
    episode_ids: List[str],
    procedure_type: str
):
    """Learn new procedure from episodic memories"""
    procedural_memory_system.learn_procedure_from_episodes(client_id, episode_ids, procedure_type)
    return {"status": "learning initiated"}

@router.get("/procedural/recommend")
async def recommend_procedure_endpoint(
    client_id: str,
    situation: str,
    top_k: int = 3
):
    """Get procedure recommendations for situation"""
    recommendations = procedural_memory_system.recommend_procedure(client_id, situation, top_k)
    return recommendations

@router.post("/procedural/execute")
async def record_execution(
    procedure_id: str,
    execution_data: ProcedureExecution
):
    """Record procedure execution results"""
    procedural_memory_system.record_procedure_execution(
        procedure_id,
        execution_data.execution_date,
        execution_data.outcome,
        execution_data.metrics
    )
    return {"status": "execution recorded"}

@router.post("/procedural/refine/{procedure_id}")
async def refine_procedure_endpoint(procedure_id: str):
    """Refine procedure based on execution history"""
    procedural_memory_system.refine_procedure(procedure_id)
    return {"status": "refinement initiated"}

@router.get("/procedural/retrieve")
async def retrieve_procedures(
    client_id: str,
    procedure_type: str = None,
    min_confidence: float = 0.0
):
    """Retrieve procedures for client"""
    procedures = procedural_memory_system.retrieve_procedures(client_id, procedure_type, min_confidence)
    return procedures
