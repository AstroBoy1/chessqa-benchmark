#!/bin/bash

#conda activate chessqa

# 3500 tasks
# 4.74 dollars
# exact accuracy of 14.6% which matches the paper's reported value

# python eval/run_openrouter.py \
#   --dataset-root benchmark \
#   --model anthropic/claude-3.5-haiku \
#   --output-dir results --workers 2 \
#   --max-tasks 3500 \
#   --max-retries 1 \
#   --max-tokens 1000

# took 13 hours, 5.7%
python eval/run_openrouter.py \
  --dataset-root benchmark \
  --model NousResearch/Meta-Llama-3-8B-Instruct \
  --output-dir results --workers 1 \
  --max-tasks 3500 \
  --max-retries 1 \
  --max-tokens 1000 \
  --url http://localhost:8000/v1/chat/completions \
  --key-path key_local.json