"""
Base Agent class for all financial advisory agents.
Provides common functionality for LLM interaction and memory access.
"""

from typing import Optional, Dict, Any, List
# Support both Fastino and MongoDB for backwards compatibility
try:
    from fastino_client import get_fastino_manager
    FASTINO_AVAILABLE = True
except ImportError:
    FASTINO_AVAILABLE = False

try:
    from database_manager import MongoDBManager
    MONGODB_AVAILABLE = True
except (ImportError, ValueError):
    MONGODB_AVAILABLE = False


class BaseFinancialAgent:
    """
    Base class for all financial advisory agents.
    Uses centralized Fireworks client and provides access to memory systems.
    """
    
    def __init__(
        self, 
        name: str, 
        role: str, 
        llama_client=None,  # Accept but ignore for backwards compatibility
        db_manager=None,  # Can be Fastino or MongoDB manager
        memory_hub: Optional[Any] = None
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            role: Agent role/description
            llama_client: Legacy parameter (ignored, uses Gemini)
            db_manager: Database manager (Fastino or MongoDB)
            memory_hub: Optional memory hub for accessing memory systems
        """
        self.name = name
        self.role = role
        self.db_manager = db_manager
        self.memory_hub = memory_hub
        
        # Initialize Linkup search client for web searching
        try:
            from linkup_client import get_linkup_search_client
            self.linkup_client = get_linkup_search_client()
        except (ImportError, ValueError) as e:
            print(f"⚠ Warning: Linkup client not available: {e}")
            self.linkup_client = None
        
        print(f"✓ Initialized agent: {name}")
    
    def execute_task(
        self, 
        prompt: str, 
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> str:
        """
        Execute a task using Google Gemini AI.
        
        Args:
            prompt: The user prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            system_message: Optional system message (overrides default)
        
        Returns:
            str: The LLM's response
        """
        try:
            # Import lazily to avoid circular dependencies
            from gemini_client import GeminiAIClient
            import config
            
            gemini_client = GeminiAIClient(model_name=config.GEMINI_MODEL)
            
            # Ensure max_tokens is an integer
            max_tokens = int(max_tokens) if max_tokens else 1024
            temperature = float(temperature) if temperature else 0.7
            
            # Use custom system message or default
            if system_message is None:
                system_message = f"You are {self.name}, a {self.role}."
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            
            import time
            attempts = 0
            last_error = None
            while attempts < 3:
                try:
                    response = gemini_client.chat_completion(
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    if isinstance(response, str) and response.strip():
                        return response
                    raise Exception("Empty response from Gemini")
                except Exception as ge:
                    last_error = ge
                    msg = str(ge)
                    if "429" in msg or "rate limit" in msg.lower():
                        time.sleep(7)
                        attempts += 1
                        continue
                    if "Empty response from Gemini" in msg:
                        messages[1]["content"] = messages[1]["content"] + "\n\nIf you cannot provide specific outputs, return a concise educational summary with 8-12 bullet points and avoid personalized advice."
                        temperature = 0.3
                        attempts += 1
                        time.sleep(2)
                        continue
                    break
            return f"Error: Could not complete task. {last_error}"
            
        except Exception as e:
            error_msg = f"✗ Error in {self.name} executing task: {e}"
            print(error_msg)
            return f"Error: Could not complete task. {e}"
    
    def search_web(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search the web using Linkup for investment strategies and information.
        
        Args:
            query: Search query
            max_results: Maximum number of results
        
        Returns:
            List of search results
        """
        if not self.linkup_client:
            return []
        
        try:
            return self.linkup_client.search(query, max_results=max_results)
        except Exception as e:
            print(f"⚠ Warning: Web search failed: {e}")
            return []
    
    def get_client_context(self, client_id: str) -> Dict[str, Any]:
        """
        Get comprehensive context for a client from memory hub.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Dictionary with client context
        """
        if not self.memory_hub:
            return {}
        
        try:
            return self.memory_hub.get_client_context(client_id)
        except Exception as e:
            print(f"⚠ Warning: Could not get client context: {e}")
            return {}
    
    def search_relevant_memories(self, client_id: str, query: str) -> Dict[str, Any]:
        """
        Search for relevant memories across all systems.
        
        Args:
            client_id: Client identifier
            query: Search query
        
        Returns:
            Dictionary with relevant memories
        """
        if not self.memory_hub:
            return {}
        
        try:
            return self.memory_hub.search_relevant_context(client_id, query)
        except Exception as e:
            print(f"⚠ Warning: Could not search memories: {e}")
            return {}
    
    def format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format client context into a string for inclusion in prompts.
        
        Args:
            context: Client context dictionary
        
        Returns:
            Formatted string
        """
        formatted_parts = []
        
        if context.get("profile"):
            profile = context["profile"]
            formatted_parts.append(
                f"Client Profile:\n"
                f"  Name: {profile.get('name', 'Unknown')}\n"
                f"  Age: {profile.get('age', 'Unknown')}\n"
                f"  Risk Tolerance: {profile.get('risk_tolerance', 'Unknown')}"
            )
        
        if context.get("portfolio"):
            portfolio = context["portfolio"]
            formatted_parts.append(
                f"\nPortfolio:\n"
                f"  Total Value: ${portfolio.get('total_value', 0):,.2f}\n"
                f"  Holdings: {portfolio.get('holdings', {})}"
            )
        
        if context.get("goals"):
            goals = context["goals"]
            if goals:
                goals_str = "\n".join([
                    f"  - {g.get('name', 'Unknown')}: ${g.get('target_amount', 0):,.2f} in {g.get('timeline', 'Unknown')}"
                    for g in goals
                ])
                formatted_parts.append(f"\nFinancial Goals:\n{goals_str}")
        
        if context.get("recent_events"):
            events = context["recent_events"][:3]  # Top 3 recent events
            if events:
                events_str = "\n".join([
                    f"  - {e.get('event_type', 'Unknown')}: {e.get('summary', e.get('transcript', 'N/A'))[:100]}"
                    for e in events
                ])
                formatted_parts.append(f"\nRecent Events:\n{events_str}")
        
        return "\n".join(formatted_parts) if formatted_parts else "No context available."