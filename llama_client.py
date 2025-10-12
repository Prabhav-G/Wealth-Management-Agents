import os
import voyageai
from fireworks.client import Fireworks

# --- Centralized Client Initialization with Lazy Loading ---
# Clients are initialized only when first accessed, not at import time.
# This allows the application to call load_dotenv() before any client initialization.

_fireworks_client = None
_voyage_client = None
_clients_initialized = False

def _initialize_clients():
    """Initialize AI clients (called lazily on first use)."""
    global _fireworks_client, _voyage_client, _clients_initialized
    
    if _clients_initialized:
        return
    
    # Get API keys from environment
    FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
    VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
    
    # Validate that keys exist
    if not FIREWORKS_API_KEY:
        raise ValueError(
            "FATAL: FIREWORKS_API_KEY not found in environment variables.\n"
            "Make sure to:\n"
            "1. Create a .env file with: FIREWORKS_API_KEY=your_key_here\n"
            "2. Call load_dotenv() before importing this module"
        )
    
    if not VOYAGE_API_KEY:
        raise ValueError(
            "FATAL: VOYAGE_API_KEY not found in environment variables.\n"
            "Make sure to:\n"
            "1. Create a .env file with: VOYAGE_API_KEY=your_key_here\n"
            "2. Call load_dotenv() before importing this module"
        )
    
    try:
        # Initialize clients
        _fireworks_client = Fireworks(api_key=FIREWORKS_API_KEY)
        _voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)
        _clients_initialized = True
        
        print("✓ Centralized Fireworks and Voyage AI clients initialized successfully.")
        
    except Exception as e:
        print(f"✗ FATAL: Failed to initialize AI clients. Error: {e}")
        raise

def get_fireworks_client():
    """Get the Fireworks AI client (initializes on first call)."""
    if not _clients_initialized:
        _initialize_clients()
    return _fireworks_client

def get_voyage_client():
    """Get the Voyage AI client (initializes on first call)."""
    if not _clients_initialized:
        _initialize_clients()
    return _voyage_client

# For backwards compatibility, create properties that auto-initialize
class _ClientProxy:
    """Proxy that initializes clients on first access."""
    
    @property
    def fireworks_client(self):
        return get_fireworks_client()
    
    @property
    def voyage_client(self):
        return get_voyage_client()

_proxy = _ClientProxy()

# Export with lazy initialization
# These will trigger initialization on first access
def __getattr__(name):
    if name == "fireworks_client":
        return get_fireworks_client()
    elif name == "voyage_client":
        return get_voyage_client()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Legacy compatibility: Export a class that can be instantiated
class FireworksAIClient:
    """Wrapper class for Fireworks AI client (for backwards compatibility)."""
    
    def __init__(self):
        """Initialize by getting the shared client."""
        self._client = get_fireworks_client()
    
    @property
    def client(self):
        return self._client
    
    def chat_completion(self, messages, temperature=None, max_tokens=None):
        """
        Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (default from config)
            max_tokens: Max tokens to generate (default from config)
        
        Returns:
            str: The model's response content
        """
        try:
            # Import config here to avoid circular imports
            import config
            
            response = self._client.chat.completions.create(
                model=config.FIREWORKS_MODEL,
                messages=messages,
                temperature=temperature or config.DEFAULT_TEMPERATURE,
                max_tokens=max_tokens or config.DEFAULT_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"✗ Error in chat completion: {e}")
            raise