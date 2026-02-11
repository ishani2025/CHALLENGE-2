import requests

print("Sending request...")

try:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "mistral",
            "messages": [
                {"role": "user", "content": "Explain OutOfMemoryError briefly."}
            ],
            "stream": False
        },
        timeout=60
    )

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

except Exception as e:
    print("Error:", e)
