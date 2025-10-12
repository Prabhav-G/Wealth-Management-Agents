from datetime import datetime
import uuid
from ai_utils import get_embedding, summarize_text, extract_tags

# In your llama_client.py or config file
import os

api_key = os.getenv("FIREWORKS_API_KEY")
if not api_key:
    raise ValueError("FIREWORKS_API_KEY environment variable not set")


class EpisodicMemory:
    def __init__(self, db_manager):
        self.collection = db_manager.db.episodic_memories

    def _generate_memory_id(self):
        return f"ep_{uuid.uuid4().hex[:12]}"

    def add_event(self, client_id: str, transcript: str, agent_source="portfolio_manager",
                related_assets=None, event_type="client_meeting", tags=None, timestamp=None):
        if related_assets is None:
            related_assets = []

        summary = summarize_text(transcript)
        if tags is None:
            tags = extract_tags(transcript)

        embedding = get_embedding(summary)
        
        # Use provided timestamp or default to current time
        event_timestamp = timestamp if timestamp is not None else datetime.utcnow()

        memory_doc = {
            "memory_id": self._generate_memory_id(),
            "client_id": client_id,
            "agent_source": agent_source,
            "timestamp": event_timestamp,  # Use the event_timestamp variable
            "event_type": event_type,
            "event_summary": summary,
            "full_transcript": transcript,
            "participants": [agent_source, "client"],
            "related_assets": related_assets,
            "embedding": embedding,
            "tags": tags,
            "importance_score": 0.5,
            "emotional_valence": "neutral",
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow(),
            "access_count": 0
        }

        self.collection.insert_one(memory_doc)
        return memory_doc

    def retrieve_memories(self, client_id: str, query: str, top_k=5):
        query_embedding = get_embedding(query)

        pipeline = [
            {"$vectorSearch": {"index": "episodic_vector_index", "path": "embedding", "queryVector": query_embedding,
                                "numCandidates": 50, "limit": top_k, "filter": {"client_id": client_id}}},
            {"$addFields": {"days_old": {"$divide": [{"$subtract": ["$$NOW", "$timestamp"]}, 86400000]}}},
            {"$addFields": {"adjusted_score": {"$multiply": ["$score", {"$exp": {"$multiply": [-1, {"$divide": ["$days_old", 30]}]}}]}}},
            {"$sort": {"adjusted_score": -1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_client_timeline(self, client_id: str, start_date, end_date):
        return list(self.collection.find(
            {"client_id": client_id, "timestamp": {"$gte": start_date, "$lte": end_date}}).sort("timestamp", 1))
