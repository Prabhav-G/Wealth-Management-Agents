
# Import the centrally managed clients from our single source of truth.
from llama_client import fireworks_client, voyage_client
import config

def summarize_text(text: str) -> str:
    """Summarize a block of text using the central Fireworks AI client."""
    prompt = f"Summarize the following text in one or two sentences:\n\n{text}"
    try:
        response = fireworks_client.chat.completions.create(
            model=config.FIREWORKS_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.DEFAULT_TEMPERATURE,
            max_tokens=200  # Summaries are short
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"✗ Error during text summarization: {e}")
        return "" # Return an empty string on failure

def extract_tags(text: str) -> list[str]:
    """Extract relevant tags from a block of text using the central Fireworks AI client."""
    prompt = f"Extract the most relevant keywords or tags from the following text. Return them as a single comma-separated string, for example: 'tag1, tag2, tag3'.\n\nText: {text}"
    try:
        response = fireworks_client.chat.completions.create(
            model=config.FIREWORKS_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, # Lower temperature for more deterministic tagging
            max_tokens=100
        )
        tags_str = response.choices[0].message.content.strip().strip('\'"')
        if not tags_str:
            return []
        return [tag.strip() for tag in tags_str.split(',')]
    except Exception as e:
        print(f"✗ Error during tag extraction: {e}")
        return [] # Return an empty list on failure

def get_embedding(text: str, model: str = "voyage-large-2-instruct") -> list[float]:
    """Get the embedding for a block of text using the central Voyage AI client."""
    try:
        result = voyage_client.embed(texts=[text], model=model)
        return result.embeddings[0]
    except Exception as e:
        print(f"✗ Error fetching embedding from Voyage AI: {e}. Returning a zero vector.")
        # A zero vector is a safer fallback than a random one.
        # The dimension for voyage-large-2-instruct is 1024.
        return [0.0] * 1024
