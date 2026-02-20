import requests
import json
import os
import logging
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=".env")
except Exception:
    pass

api_key = os.getenv("SCALEDOWN_API_KEY")
class ScaleDownClient:
    def __init__(self, timeout: int = 10):
        self.url = "https://api.scaledown.xyz/compress/raw/"
        self.api_key = os.getenv("SCALEDOWN_API_KEY")
        self.timeout = timeout
    def deterministic_compress(self, log: str) -> str:
        lines = log.splitlines()

        important_lines = []
        caused_by_lines = []

        for line in lines:
            line = line.strip()
            if "Exception" in line or "Error" in line:
                important_lines.append(line)
            if line.startswith("Caused by"):
                caused_by_lines.append(line)
            if line.startswith("at ") and len(important_lines) < 15:
                important_lines.append(line)

        compressed = "\n".join(important_lines + caused_by_lines)

        return compressed if compressed else log[:1000]
    def scaledown_compress(self, log: str) -> str:
        if not self.api_key:
            logging.warning("ScaleDown API key missing. Using deterministic compression only.")
            return log

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
            }

        payload = {
            "text": log
        }
        print("Sending request to:", self.url)
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json().get("compressed_text", log)
            else:
                logging.warning(f"ScaleDown failed: {response.status_code}")
                return log

        except Exception as e:
            logging.warning(f"ScaleDown exception: {e}")
            return log
    def compress(self, log: str) -> str:
        original_length = len(log)
        deterministic = self.deterministic_compress(log)
        final_output = self.scaledown_compress(deterministic)
        compressed_length = len(final_output)
        ratio = compressed_length / original_length if original_length > 0 else 1
        logging.info(f"Hybrid compression ratio: {ratio:.3f}")
        return final_output, ratio
        