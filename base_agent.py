from llama_client import FireworksAIClient
from database_manager import MongoDBManager

class BaseFinancialAgent:
    def __init__(self, name: str, role: str, llama_client: FireworksAIClient, db_manager: MongoDBManager, memory_hub=None):
        self.name = name
        self.role = role
        self.llama_client = llama_client
        self.db_manager = db_manager
        # Accept memory_hub as an argument to break the circular import
        self.memory_hub = memory_hub

    def execute_task(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7):
        """Executes a task using the Llama model."""
        response = self.llama_client.client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p1-70b-instruct",
            messages=[
                {"role": "system", "content": f"You are {self.name}, a {self.role}."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
