
from typing import List, Dict
from openai import OpenAI
import config

from dotenv import load_dotenv

load_dotenv()


class FireworksAIClient:
    """Fireworks AI Client for Llama models"""

    def __init__(self):
        """Initialize Fireworks AI client and verify the API key."""
        api_key = config.fw_3ZhDcC6YgP5yvHmqYwiagMPx

        # Securely print a confirmation of the key being used.
        if api_key and len(api_key) > 8:
            print(f"✓ Using Fireworks API Key ending in '...{api_key[-4:]}'")
        else:
            print("✗ FATAL: Fireworks API Key not found or is invalid in the environment.")
            # Stop the application if the key is missing.
            raise ValueError("Fireworks API Key is missing or invalid.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=config.FIREWORKS_BASE_URL
        )
        self.model = config.FIREWORKS_MODEL
        print(f"✓ Initialized Fireworks AI client with model: {self.model}")

    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       temperature: float = None,
                       max_tokens: int = None) -> str:
        """Call Fireworks AI for chat completion"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or config.DEFAULT_TEMPERATURE,
                max_tokens=max_tokens or config.DEFAULT_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            # The original exception from the library is more informative.
            print(f"✗ An error occurred while communicating with the Fireworks AI API.")
            raise e
