#  hf auth login
# pip install accelerate
# uses 15GB

import transformers
import torch

model_id = "meta-llama/Llama-3.1-8B"

pipeline = transformers.pipeline(
    "text-generation", model=model_id, model_kwargs={"dtype": torch.bfloat16}, device_map="auto"
)

print(pipeline("What moves can white make in the starting chess position?"))
