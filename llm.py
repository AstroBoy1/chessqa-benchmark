#  hf auth login
# pip install accelerate
# pip install bitsandbytes
# uses 15GB

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

torch.manual_seed(0)

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a chess expert."},
    {"role": "user", "content": "When should you castle in chess?"},
]

return_output = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True
).to(model.device)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

input_ids = return_output["input_ids"]
attention_mask = return_output["attention_mask"]

outputs = model.generate(
    input_ids,
    attention_mask=attention_mask,
    max_new_tokens=512,
    eos_token_id=terminators,
    do_sample=False,
)
response = outputs[0][input_ids.shape[-1]:]
print(tokenizer.decode(response, skip_special_tokens=True))
