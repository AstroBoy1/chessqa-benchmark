# TODO: hook this into chessqa benchmarking script later

import requests

URL = "http://localhost:8000/v1/chat/completions"   # default vLLM endpoint
API_KEY = "token-abc123"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

model_name = "NousResearch/Meta-Llama-3-8B-Instruct"
model_name = "/nfs/stak/users/omorim/hpc-share/omorim/projects/chess_explanation/models/llama3-qlora"
payload = {
    "model": model_name,
    "messages": [
        {"role": "user", "content": "Explain chess."}
    ],
    "max_tokens": 500,
    "temperature": 0,
}

response = requests.post(URL, json=payload, headers=headers)
print(response.json())
