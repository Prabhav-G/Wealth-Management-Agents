import os
import time
import requests
from dotenv import load_dotenv
from llama_client import FireworksAIClient

# Load environment variables
load_dotenv()

# Initialize clients
fireworks_client = FireworksAIClient()
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

def robust_post(url: str, headers: dict, payload: dict, max_attempts: int = 3, backoff: float = 2.0):
    """Robust POST request function with exponential backoff."""
    attempt = 0
    while attempt < max_attempts:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error on attempt {attempt + 1}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed on attempt {attempt + 1}: {e}")
        
        time.sleep(backoff ** attempt)
        attempt += 1
    raise ConnectionError(f"Failed to connect to {url} after {max_attempts} attempts.")

def summarize_text(text: str) -> str:
    """Summarize a block of text using the Fireworks AI model."""
    prompt = f"Summarize the following text in one or two sentences:\n\n{text}"
    return fireworks_client.chat_completion([{"role": "user", "content": prompt}])

def extract_tags(text: str) -> list[str]:
    """Extract relevant tags from a block of text using Fireworks AI."""
    prompt = f"Extract the most relevant keywords or tags from the following text. Return them as a comma-separated list. For example: 'tag1, tag2, tag3'\n\nText: {text}"
    tags_str = fireworks_client.chat_completion([{"role": "user", "content": prompt}])
    return [tag.strip() for tag in tags_str.split(',')]

def get_embedding(text: str, model: str = "voyage-large-2-instruct") -> list[float]:
    """Get the embedding for a block of text using Voyage AI."""
    if not VOYAGE_API_KEY:
        print("Warning: VOYAGE_API_KEY not found. Returning a random embedding.")
        import random
        return [random.random() for _ in range(1024)]

    url = "https://api.voyageai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {VOYAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"input": text, "model": model}
    
    try:
        response_data = robust_post(url, headers, payload)
        if "data" in response_data and response_data["data"]:
            return response_data["data"][0]["embedding"]
        else:
            raise ValueError("Invalid response from Voyage AI.")
    except (ConnectionError, ValueError) as e:
        print(f"Error fetching embedding: {e}. Falling back to random embedding.")
        import random
        return [random.random() for _ in range(1024)]
