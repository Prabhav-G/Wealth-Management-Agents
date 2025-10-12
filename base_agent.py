"""
Base Agent class for all financial advisory agents.
Provides common functionality for LLM interaction and memory access.
"""

from typing import Optional, Dict, Any
from database_manager import MongoDBManager


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
        db_manager: MongoDBManager = None,
        memory_hub: Optional[Any] = None
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            role: Agent role/description
            llama_client: Legacy parameter (ignored, uses centralized client)
            db_manager: MongoDB database manager
            memory_hub: Optional memory hub for accessing memory systems
        """
        self.name = name
        self.role = role
        self.db_manager = db_manager
        self.memory_hub = memory_hub
        
        print(f"✓ Initialized agent: {name}")
    
    def execute_task(
        self, 
        prompt: str, 
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> str:
        """
        Execute a task using the centralized Fireworks AI client.
        
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
            from llama_client import get_fireworks_client
            import config
            
            fireworks_client = get_fireworks_client()
            
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
            
            response = fireworks_client.chat.completions.create(
                model=config.FIREWORKS_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"✗ Error in {self.name} executing task: {e}"
            print(error_msg)
            return f"Error: Could not complete task. {e}"
    
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