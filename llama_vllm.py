# module load cuda/12.8

# conda create -n llama_vllm python=3.12 -y
# conda activate llama_vllm

# pip install vllm

# run in terminal
# vllm serve NousResearch/Meta-Llama-3-8B-Instruct \
#   --dtype auto \
#   --api-key token-abc123


vllm serve /nfs/stak/users/omorim/hpc-share/omorim/projects/chess_explanation/models/llama3-qlora \
--api-key token-abc123