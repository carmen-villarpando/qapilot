"""
Ollama client for local LLM inference - ZERO COST solution
"""

import json
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with local Ollama instance."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 60  # 60 seconds timeout
    
    def generate_response(self, prompt: str, model: str = "phi3.5") -> str:
        """Generate response using local Ollama model."""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to Ollama: {e}")
            return None
    
    def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama registry."""
        try:
            payload = {"name": model}
            
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=300  # 5 minutes for model download
            )
            
            return response.status_code == 200
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error pulling model {model}: {e}")
            return False
    
    def list_models(self) -> list:
        """List available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return [model["name"] for model in result.get("models", [])]
            else:
                return []
                
        except requests.exceptions.RequestException:
            return []
    
    def is_model_available(self, model: str) -> bool:
        """Check if a model is available."""
        models = self.list_models()
        return model in models
