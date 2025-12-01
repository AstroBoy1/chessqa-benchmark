#  hf auth login
# pip install accelerate
# pip install bitsandbytes
# uses 15GB

import transformers
import torch

# model_id = "meta-llama/Llama-3.1-8B"

# pipeline = transformers.pipeline(
#     "text-generation", model=model_id, model_kwargs={"dtype": torch.bfloat16}, device_map="auto"
# )

# print(pipeline("What moves can white make in the starting chess position?"))

# 51GB
# Use a pipeline as a high-level helper
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# Quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# Load TEXT-ONLY model (no vision tower)
model_id = "google/gemma-3-27b-it"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)

# Text-only input
prompt = "List all legal moves for White from the starting chess position."

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

with torch.inference_mode():
    output_ids = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=False
    )

print(tokenizer.decode(output_ids[0], skip_special_tokens=True))
