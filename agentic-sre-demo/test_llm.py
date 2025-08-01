import os
from dotenv import load_dotenv
import httpx

# Load your key
load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")
if not key:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")

# Use the correct base URL here:
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello"}
    ]
}

# Send the request
resp = httpx.post(url, headers=headers, json=payload, timeout=30.0)
resp.raise_for_status()

message = resp.json()["choices"][0]["message"]["content"]
print("LLM responded:", message)
