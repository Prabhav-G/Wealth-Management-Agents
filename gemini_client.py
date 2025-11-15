"""
Google Gemini AI Client
Replaces Fireworks/Llama for LLM operations
"""
import os
import google.generativeai as genai
from typing import List, Dict, Optional

_gemini_client = None
_gemini_initialized = False

def _initialize_gemini():
    """Initialize Gemini client (called lazily on first use)."""
    global _gemini_client, _gemini_initialized
    
    if _gemini_initialized:
        return
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        raise ValueError(
            "FATAL: GEMINI_API_KEY not found in environment variables.\n"
            "Make sure to:\n"
            "1. Create a .env file with: GEMINI_API_KEY=your_key_here\n"
            "2. Get your API key from: https://makersuite.google.com/app/apikey"
        )
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_client = genai.GenerativeModel('gemini-pro')
        _gemini_initialized = True
        print("✓ Gemini AI client initialized successfully.")
    except Exception as e:
        print(f"✗ FATAL: Failed to initialize Gemini client. Error: {e}")
        raise

def get_gemini_client():
    """Get the Gemini AI client (initializes on first call)."""
    if not _gemini_initialized:
        _initialize_gemini()
    return _gemini_client

def get_gemini_model(model_name: str = "gemini-pro"):
    """Get a specific Gemini model."""
    if not _gemini_initialized:
        _initialize_gemini()
    return genai.GenerativeModel(model_name)

class GeminiAIClient:
    """Wrapper class for Gemini AI client (for backwards compatibility)."""
    
    def __init__(self, model_name: str = "gemini-pro"):
        """Initialize by getting the shared client."""
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        if self._model is None:
            self._model = get_gemini_model(self.model_name)
        return self._model
    
    def chat_completion(self, messages: List[Dict], temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """
        Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Max tokens to generate
        
        Returns:
            str: The model's response content
        """
        try:
            # Convert messages format for Gemini
            # Build a combined prompt from messages
            prompt_parts = []
            system_message = None
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    system_message = content
                elif role == "user":
                    if system_message:
                        # Include system message before user message
                        prompt_parts.append(f"{system_message}\n\n{content}")
                        system_message = None  # Only use once
                    else:
                        prompt_parts.append(content)
                elif role == "assistant":
                    prompt_parts.append(f"Previous response: {content}")
            
            # Combine all parts
            full_prompt = "\n\n".join(prompt_parts)
            if system_message:
                full_prompt = f"{system_message}\n\n{full_prompt}"
            
            # Generate configuration
            generation_config = {}
            if temperature is not None:
                generation_config["temperature"] = min(max(temperature, 0.0), 1.0)
            if max_tokens is not None:
                generation_config["max_output_tokens"] = max_tokens
            
            # Generate response
            if generation_config:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
            else:
                response = self.model.generate_content(full_prompt)
            
            return response.text if hasattr(response, 'text') else str(response)
            
        except Exception as e:
            print(f"✗ Error in Gemini chat completion: {e}")
            raise

# For backwards compatibility
def __getattr__(name):
    if name == "gemini_client":
        return get_gemini_client()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

