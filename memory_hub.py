
from episodic_memory.episodic_memory import EpisodicMemory
import semantic_memory.memory as semantic_memory_functions
from procedural_memory.procedural_memory import ProceduralMemorySystem
from database_manager import MongoDBManager

# Create a simple namespace object to hold the semantic memory functions
class SemanticMemoryWrapper:
    def __init__(self):
        self.create = semantic_memory_functions.create_semantic_memory
        self.retrieve = semantic_memory_functions.retrieve_semantic_memories
        self.update = semantic_memory_functions.update_semantic_memory
        self.check_consistency = semantic_memory_functions.check_consistency

class MemoryHub:
    def __init__(self, db_manager: MongoDBManager):
        self.episodic = EpisodicMemory(db_manager)
        # Use the wrapper instead of the non-existent class
        self.semantic = SemanticMemoryWrapper()
        self.procedural = ProceduralMemorySystem(db_manager)

    def get_memory_systems(self):
        return {
            'episodic': self.episodic,
            'semantic': self.semantic,
            'procedural': self.procedural
        }
