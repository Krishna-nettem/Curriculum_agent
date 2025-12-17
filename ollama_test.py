import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TIMEOUT = 120


def call_ollama(prompt: str, model_name: str = "llama3.1:8b", timeout: int = OLLAMA_TIMEOUT) -> str:
    """Call local Ollama HTTP API. Raises on failure."""
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        r.raise_for_status()
        j = r.json()
        
        text = j.get("response") or j.get("output") or str(j)
        
        return text
    except Exception:
        
        raise

topic = "Generative AI for Beginners"


if __name__ == "__main__":
    md = call_ollama(topic)

    print(md)