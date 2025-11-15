from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file at the module level
load_dotenv()

# Try to import Fastino first (preferred)
try:
    from fastino_client import get_fastino_manager
    FASTINO_AVAILABLE = True
except (ImportError, ValueError):
    FASTINO_AVAILABLE = False

# MongoDB as fallback
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure
    import certifi
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

class DatabaseManager:
    """Unified database manager that uses Fastino by default, MongoDB as fallback."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Use object.__setattr__ to avoid triggering __getattr__
        object.__setattr__(self, 'initialized', False)
        
        if hasattr(self, 'initialized') and self.initialized:
            return

        # Try Fastino first
        if FASTINO_AVAILABLE:
            try:
                manager = get_fastino_manager()
                object.__setattr__(self, 'manager', manager)
                object.__setattr__(self, 'db_type', "fastino")
                object.__setattr__(self, 'initialized', True)
                print("✓ Using Fastino for user profiles")
                return
            except Exception as e:
                print(f"⚠ Fastino initialization failed: {e}")
                print("  Falling back to MongoDB...")

        # Fallback to MongoDB
        if MONGODB_AVAILABLE:
            try:
                manager = MongoDBManager()
                object.__setattr__(self, 'manager', manager)
                object.__setattr__(self, 'db_type', "mongodb")
                object.__setattr__(self, 'initialized', True)
                print("✓ Using MongoDB (fallback)")
                return
            except Exception as e:
                print(f"⚠ MongoDB initialization failed: {e}")

        # If both fail, raise error
        raise ValueError(
            "Neither Fastino nor MongoDB could be initialized. "
            "Please set FASTINO_API_KEY or MONGODB_URL in your .env file."
        )

    def __getattr__(self, name):
        """Delegate to the underlying manager, but avoid recursion."""
        # Check if we have the manager attribute directly
        if 'manager' in self.__dict__:
            return getattr(self.__dict__['manager'], name)
        # If manager doesn't exist, raise AttributeError
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

# Legacy MongoDBManager for backwards compatibility
class MongoDBManager:
    """Manages a singleton MongoDB connection."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'client') and self.client:
            return

        connection_string = os.getenv("MONGODB_URL")
        database_name = os.getenv("DATABASE_NAME", "financial_advisory_system")

        if not connection_string:
            print("✗ FATAL: MONGODB_URL environment variable not set.")
            print("  Please ensure your .env file is correctly configured.")
            raise ValueError("MONGODB_URL not found.")

        print("Attempting to connect to MongoDB Atlas...")
        try:
            self.client = MongoClient(connection_string, tlsCAFile=certifi.where())
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            print(f"✓ Successfully connected to MongoDB database '{database_name}'")
            self._create_search_indexes()

        except (ConnectionFailure, OperationFailure) as e:
            print(f"✗ FATAL: Failed to connect to MongoDB: {e}")
            print("  Please check your environment and configuration.")
            raise

    def __getattr__(self, name):
        """
        Dynamically provide access to MongoDB collections.
        
        This allows accessing collections as attributes:
            self.market_research -> self.db["market_research"]
            self.semantic_memories -> self.db["semantic_memories"]
        
        Args:
            name: Collection name
        
        Returns:
            MongoDB collection object
        """
        # Avoid infinite recursion for special attributes
        if name.startswith('_') or name in ['db', 'client']:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        # Check if db exists (to avoid issues during initialization)
        if hasattr(self, 'db'):
            return self.db[name]
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def _create_search_indexes(self):
        """Create vector search indexes if they don't exist."""
        self._create_vector_index(
            collection_name="episodic_memories",
            index_name="episodic_vector_index",
            field_name="embedding",
            dimensions=1024,
            similarity="cosine"
        )

    def _create_vector_index(self, collection_name: str, index_name: str, field_name: str, dimensions: int, similarity: str):
        """Helper to create a single vector search index, creating the collection if needed."""
        try:
            # Get a list of existing collection names
            existing_collections = self.db.list_collection_names()
            collection = self.db[collection_name]

            # If the collection does not exist, create it.
            if collection_name not in existing_collections:
                self.db.create_collection(collection_name)
                print(f"Info: Collection '{collection_name}' did not exist and was created.")

            indexes = list(collection.list_search_indexes(name=index_name))
            if indexes:
                print(f"✓ Search index '{index_name}' on '{collection_name}' already exists.")
                return

            print(f"Creating search index '{index_name}' on collection '{collection_name}'...")
            
            index_model = {
                "name": index_name,
                "definition": {
                    "mappings": {
                        "dynamic": True,
                        "fields": {
                            field_name: {
                                "type": "vector",
                                "dimension": dimensions,
                                "similarity": similarity
                            }
                        }
                    }
                }
            }
            collection.create_search_index(model=index_model)

            print(f"✓ Successfully created search index '{index_name}'.")

        except OperationFailure as e:
            print(f"✗ WARNING: Could not create or verify search index '{index_name}'.")
            print(f"  Reason: {e.details.get('errmsg', str(e))}")
            print("  Vector search functionality will not work for this collection.")
            print("  Please ensure you are connected to a MongoDB Atlas cluster with search nodes enabled.")

# Instantiate a singleton connection object that can be imported across the application
# Uses Fastino by default, MongoDB as fallback
try:
    mongo_db_manager = DatabaseManager()
except ValueError:
    # If DatabaseManager fails, try MongoDB directly for backwards compatibility
    try:
        mongo_db_manager = MongoDBManager()
    except Exception:
        mongo_db_manager = None
        print("⚠ Warning: No database manager available. Some features may not work.")