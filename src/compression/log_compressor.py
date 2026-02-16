import requests
import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


class ScaleDownClient:

    def __init__(self, timeout: int = 10, max_retries: int = 2):
        self.url = "https://api.scaledown.xyz/compress/raw/"
        self.api_key = os.getenv("SCALEDOWN_API_KEY")
        self.timeout = timeout
        self.max_retries = max_retries

        if not self.api_key:
            raise ValueError("SCALEDOWN_API_KEY not found in environment variables")

    def compress(self, structured_log: str):

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "context": structured_log,
            "prompt": (
                "Tighten this structured stack trace further. "
                "Preserve exception type, caused-by chain, "
                "and the most relevant stack frames only."
            ),
            "scaledown": {
                "rate": "aggressive"
            }
        }

        attempt = 0

        while attempt < self.max_retries:
            try:
                response = requests.post(
                    self.url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=self.timeout
                )

                if response.status_code != 200:
                    logging.warning(f"ScaleDown HTTP error: {response.status_code}")
                    attempt += 1
                    continue

                result = response.json()

                if result.get("successful"):
                    compressed = result["results"]["compressed_prompt"]
                    ratio = result["results"]["compression_ratio"]

                    logging.info(f"ScaleDown compression ratio: {ratio}")
                    return compressed, ratio

                logging.warning("ScaleDown API returned unsuccessful response.")
                attempt += 1

            except requests.exceptions.RequestException as e:
                logging.warning(f"ScaleDown request failed: {e}")
                attempt += 1

        logging.warning("ScaleDown failed after retries. Falling back.")
        return structured_log, 1.0
