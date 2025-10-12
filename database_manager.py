
from typing import Dict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv
import certifi

# Load environment variables from .env file at the module level
load_dotenv()

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
mongo_db_manager = MongoDBManager()
