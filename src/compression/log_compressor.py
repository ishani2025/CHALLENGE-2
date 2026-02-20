import requests
import json
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO)

class ScaleDownClient:

    def __init__(self, timeout: int = 10, max_retries: int = 2):
        self.url = "https://api.scaledown.xyz/compress/raw/"
        self.timeout = timeout
        self.max_retries = max_retries

        self.api_key = st.secrets.get("SCALEDOWN_API_KEY")

        if not self.api_key:
            st.warning("ScaleDown key not configured. Running in fallback mode.")

    def compress(self, structured_log: str):

        if not self.api_key:
            return structured_log, 1.0

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
                    attempt += 1
                    continue

                result = response.json()

                if result.get("successful"):
                    compressed = result["results"]["compressed_prompt"]
                    ratio = result["results"]["compression_ratio"]
                    return compressed, ratio

                attempt += 1

            except requests.exceptions.RequestException:
                attempt += 1

        return structured_log, 1.0