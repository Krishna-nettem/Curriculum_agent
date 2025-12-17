import os
import requests
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger()
load_dotenv()


try:
    from google import generativeai as genai
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
        logger.info("Gemini SDK configured from GEMINI_API_KEY")
    else:
        logger.warning("GEMINI_API_KEY missing in env; Gemini calls will fail until provided.")
    
    try:
        model = genai.GenerativeModel("models/gemini-flash-latest")
        logger.info("Gemini model instantiated")
    except Exception:
        model = None
        logger.exception("Failed to instantiate Gemini model object")
except Exception:
    genai = None
    model = None
    logger.exception("Failed to import google.generativeai SDK; Gemini unavailable")


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TIMEOUT = 140


def call_gemini(prompt: str) -> str:
    """Call Gemini model. Raises on failure."""
    if model is None:
        raise RuntimeError("Gemini model not configured or SDK missing.")
    try:
        logger.info("Calling Gemini")
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", None) or str(resp)
        logger.info("Gemini call succeeded")
        return text
    except Exception:
        logger.exception("Gemini call failed")
        raise


def call_ollama(prompt: str, model_name: str = "llama3.1:8b", timeout: int = OLLAMA_TIMEOUT) -> str:

    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        r.raise_for_status()
        j = r.json()
        
        text = j.get("response") or j.get("output") or str(j)
        logger.info("Ollama call succeeded")
        return text
    except Exception:
        logger.exception("Ollama call failed")
        raise

# To test this bad boy directly
'''def generate_with_fallback(prompt: str, prefer_gemini: bool = True) -> str:
    
    
    if prefer_gemini and model is not None:
        try:
            return call_gemini(prompt)
        except Exception:
            logger.warning("Gemini failed; falling back to Ollama")
            try:
                return call_ollama(prompt)
            except Exception:
                logger.exception("Both Gemini and Ollama failed")
                return "ERROR: Both Gemini and Ollama failed to generate content. Check logs.json."
    
    try:
        return call_ollama(prompt)
    except Exception:
        logger.warning("Ollama failed; trying Gemini (if available)")
        try:
            return call_gemini(prompt)
        except Exception:
            logger.exception("Both Ollama and Gemini failed")
            return "ERROR: Both Ollama and Gemini failed to generate content. Check logs.json."


# To test this bad boy directly
if __name__ == "__main__":
    test_prompt = "Create a short outline for a Photography course in markdown (3 modules)."
    out = generate_with_fallback(test_prompt)
    
    print(out)'''
