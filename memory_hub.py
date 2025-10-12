"""
Memory Hub - Centralized access point for all memory systems.
Provides a unified interface to semantic, episodic, and procedural memory.
"""

from typing import List, Dict, Any
from datetime import datetime


class SemanticMemoryWrapper:
    """Wrapper for semantic memory operations."""
    
    def __init__(self):
        # Lazy import to avoid circular dependencies
        pass
    
    def retrieve(self, client_id: str, memory_type: str = None) -> List[Dict]:
        """
        Retrieve semantic memories for a client.
        
        Args:
            client_id: Client identifier
            memory_type: Optional filter by memory type (profile, portfolio, goals)
        
        Returns:
            List of semantic memory documents
        """
        try:
            from semantic_memory import memory as semantic_memory
            return semantic_memory.retrieve_semantic_memories(client_id, memory_type)
        except Exception as e:
            # Fallback to direct database query
            from database_manager import MongoDBManager
            db = MongoDBManager()
            
            query = {"client_id": client_id, "is_active": True}
            if memory_type:
                query["memory_type"] = memory_type
            
            return list(db.db.semantic_memories.find(query))
    
    def create(self, client_id: str, memory_type: str, memory_value: Any) -> str:
        """
        Create a new semantic memory.
        
        Args:
            client_id: Client identifier
            memory_type: Type of memory (profile, portfolio, goals)
            memory_value: The actual memory content
        
        Returns:
            ID of created memory
        """
        try:
            from semantic_memory import memory as semantic_memory
            return semantic_memory.create_semantic_memory(client_id, memory_type, memory_value)
        except AttributeError:
            # Fallback: direct database insertion
            from database_manager import MongoDBManager
            db = MongoDBManager()
            
            doc = {
                "client_id": client_id,
                "memory_type": memory_type,
                "memory_value": memory_value,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = db.db.semantic_memories.insert_one(doc)
            return str(result.inserted_id)
    
    def get_profile(self, client_id: str) -> Dict:
        """Get client profile."""
        memories = self.retrieve(client_id, "profile")
        if memories and len(memories) > 0:
            # Return the data field if it exists, otherwise memory_value
            return memories[0].get("data") or memories[0].get("memory_value", {})
        return {}
    
    def get_portfolio(self, client_id: str) -> Dict:
        """Get client portfolio."""
        memories = self.retrieve(client_id, "portfolio")
        if memories and len(memories) > 0:
            return memories[0].get("data") or memories[0].get("memory_value", {})
        return {}
    
    def get_goals(self, client_id: str) -> List[Dict]:
        """Get client goals."""
        memories = self.retrieve(client_id, "goals")
        return [m.get("data") or m.get("memory_value", {}) for m in memories]


class EpisodicMemoryWrapper:
    """Wrapper for episodic memory operations."""
    
    def __init__(self):
        pass
    
    def retrieve(self, client_id: str, event_type: str = None, limit: int = 10) -> List[Dict]:
        """
        Retrieve episodic memories for a client.
        
        Args:
            client_id: Client identifier
            event_type: Optional filter by event type
            limit: Maximum number of events to retrieve
        
        Returns:
            List of episodic memory documents
        """
        from database_manager import MongoDBManager
        db = MongoDBManager()
        
        query = {"client_id": client_id}
        if event_type:
            query["event_type"] = event_type
        
        return list(db.db.episodic_memories.find(query).sort("timestamp", -1).limit(limit))
    
    def search(self, client_id: str, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Semantic search through episodic memories.
        
        Args:
            client_id: Client identifier
            query_text: Search query
            top_k: Number of results to return
        
        Returns:
            List of relevant episodic memories
        """
        try:
            from episodic_memory import episodic_memory
            from database_manager import MongoDBManager
            
            db = MongoDBManager()
            manager = episodic_memory.EpisodicMemory(db)
            
            if hasattr(manager, 'search_episodes'):
                return manager.search_episodes(client_id, query_text, top_k)
            elif hasattr(manager, 'retrieve_relevant_episodes'):
                return manager.retrieve_relevant_episodes(client_id, query_text, top_k)
            else:
                # Fallback: just return recent episodes
                return self.retrieve(client_id, limit=top_k)
        except Exception as e:
            print(f"⚠ Warning: Episodic search failed, using fallback. Error: {e}")
            return self.retrieve(client_id, limit=top_k)
    
    def add(self, client_id: str, event_type: str, transcript: str, 
            timestamp: datetime = None, agent_source: str = None) -> str:
        """
        Add a new episodic memory.
        
        Args:
            client_id: Client identifier
            event_type: Type of event
            transcript: Event transcript/description
            timestamp: Event timestamp (defaults to now)
            agent_source: Source agent that generated this event
        
        Returns:
            ID of created memory
        """
        try:
            from episodic_memory import episodic_memory
            from database_manager import MongoDBManager
            
            db = MongoDBManager()
            manager = episodic_memory.EpisodicMemory(db)
            
            result = manager.add_event(
                client_id=client_id,
                event_type=event_type,
                transcript=transcript,
                timestamp=timestamp or datetime.utcnow()
            )
            return str(result.get("_id", ""))
        except Exception as e:
            print(f"⚠ Warning: Could not add episodic memory: {e}")
            return ""
    
    def add_event(self, client_id: str, content: str, agent_source: str = None, 
                  event_type: str = "analysis", timestamp: datetime = None, **kwargs) -> str:
        """
        Add event (compatible signature for orchestrator).
        Accepts both old and new parameter names for backwards compatibility.
        
        Args:
            client_id: Client identifier
            content: Event content/transcript (can also be passed as 'transcript')
            agent_source: Source agent
            event_type: Type of event
            timestamp: Event timestamp
            **kwargs: Additional arguments (for backwards compatibility)
        
        Returns:
            ID of created memory
        """
        # Handle if 'transcript' was passed instead of 'content'
        transcript = kwargs.get('transcript', content)
        
        return self.add(
            client_id=client_id,
            event_type=event_type,
            transcript=f"[{agent_source}] {transcript}" if agent_source else transcript,
            timestamp=timestamp
        )


class ProceduralMemoryWrapper:
    """Wrapper for procedural memory operations."""
    
    def __init__(self):
        pass
    
    def retrieve(self, procedure_type: str = None, min_confidence: float = 0.0) -> List[Dict]:
        """
        Retrieve procedural memories.
        
        Args:
            procedure_type: Optional filter by procedure type
            min_confidence: Minimum confidence score
        
        Returns:
            List of procedural memory documents
        """
        from database_manager import MongoDBManager
        db = MongoDBManager()
        
        query = {"confidence_score": {"$gte": min_confidence}}
        if procedure_type:
            query["procedure_type"] = procedure_type
        
        return list(db.db.procedural_memories.find(query).sort("confidence_score", -1))
    
    def get_by_name(self, procedure_name: str) -> Dict:
        """Get a specific procedure by name."""
        from database_manager import MongoDBManager
        db = MongoDBManager()
        
        return db.db.procedural_memories.find_one({"procedure_name": procedure_name})
    
    def search(self, situation: str, top_k: int = 3) -> List[Dict]:
        """
        Find relevant procedures for a situation.
        
        Args:
            situation: Description of current situation
            top_k: Number of procedures to return
        
        Returns:
            List of relevant procedures
        """
        # For now, return top procedures by confidence
        # In production, this would use vector search
        return self.retrieve()[:top_k]


class MemoryHub:
    """
    Central hub for accessing all memory systems.
    Provides a unified interface for the orchestrator.
    """
    
    def __init__(self, db_manager=None):
        """
        Initialize the memory hub.
        
        Args:
            db_manager: Database manager instance (optional, for compatibility)
        """
        self.db_manager = db_manager
        
        # Initialize memory wrappers
        self.semantic = SemanticMemoryWrapper()
        self.episodic = EpisodicMemoryWrapper()
        self.procedural = ProceduralMemoryWrapper()
        
        print("✓ Memory Hub initialized")
    
    def get_client_context(self, client_id: str) -> Dict[str, Any]:
        """
        Get comprehensive context for a client.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Dictionary with profile, portfolio, goals, and recent events
        """
        return {
            "profile": self.semantic.get_profile(client_id),
            "portfolio": self.semantic.get_portfolio(client_id),
            "goals": self.semantic.get_goals(client_id),
            "recent_events": self.episodic.retrieve(client_id, limit=5)
        }
    
    def search_relevant_context(self, client_id: str, query: str) -> Dict[str, Any]:
        """
        Search for relevant context across all memory types.
        
        Args:
            client_id: Client identifier
            query: User query
        
        Returns:
            Dictionary with relevant memories from all systems
        """
        return {
            "semantic": self.semantic.retrieve(client_id),
            "episodic": self.episodic.search(client_id, query, top_k=3),
            "procedural": self.procedural.search(query, top_k=3)
        }