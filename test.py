import requests
import json

OPENROUTER_API_KEY= "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"

model = "anthropic/claude-3.5-haiku"
model2 = "openai/gpt-4o"

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer " + OPENROUTER_API_KEY,
  },
  data=json.dumps({
    "model": model, # Optional
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ],
    "max_tokens": 100,
  })
)

print(response.json())