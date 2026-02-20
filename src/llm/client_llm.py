import requests
from typing import Optional, Dict, Any
from datetime import datetime

class OllamaClient:
    """Client for interacting with Ollama LLM service."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama service URL
            model: Model name to use
        """
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate response from Ollama.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Ollama: {str(e)}")
    
    def chat(self, messages: list, **kwargs) -> str:
        """Generate response from chat messages."""
        chat_endpoint = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(chat_endpoint, json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Ollama chat: {str(e)}")