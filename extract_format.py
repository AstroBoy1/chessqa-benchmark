# read json file
# conda install chess

import json
from typing import Dict, Any
import chess

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
fn = "results/NousResearch_Meta-Llama-3-8B-Instruct_pretty.json"
data = read_json_file(fn)
pairs = []

# returns piece arrangement and legal moves from FEN, off by default
def get_context(fen: str) -> str:
    """Generate chess context from FEN.

    Some dataset entries append move hints after a pipe ("|") like:
    "<FEN> | e2e4 e7e5". Strip that part before parsing.
    """
    fen_clean = fen.split('|', 1)[0].strip()
    try:
        board = chess.Board(fen_clean)
    except Exception:
        # Fallback: try to coerce whitespace and retry; otherwise return minimal context
        try:
            board = chess.Board(" ".join(fen_clean.split()))
        except Exception:
            return ""

    # Piece arrangement
    pieces = {}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = "White" if piece.color == chess.WHITE else "Black"
            names = {1: "Pawn", 2: "Knight", 3: "Bishop", 4: "Rook", 5: "Queen", 6: "King"}
            key = f"{color} {names[piece.piece_type]}"
            if key not in pieces:
                pieces[key] = []
            pieces[key].append(chess.square_name(square))

    arrangement = ", ".join(f"{k}: {v}" for k, v in pieces.items())
    legal_moves = ", ".join(sorted(move.uci() for move in board.legal_moves))

    return f"Piece arrangement: {arrangement}\nLegal moves: {legal_moves}\n\n"

# called for each question
def format_prompt(task: Dict[str, Any], add_context: bool = False, format_example_group: int = 1) -> str:
    """Format task into prompt."""
    question = task['question']
    if add_context and 'input' in task:
        context = get_context(task['input'])
        question = question.replace('CONTEXT_PLACEHOLDER', context)
    else:
        question = question.replace('CONTEXT_PLACEHOLDER', '')

    if 'format_examples' in task and task['format_examples']:
        examples_list = task['format_examples']
        if len(examples_list) >= 2:
            # Select specific example based on group (1 or 2)
            if format_example_group == 2 and len(examples_list) >= 2:
                example = examples_list[1]
            else:
                example = examples_list[0]
        else:
            # Fallback to first/only example
            example = examples_list[0] if examples_list else ""
        question = question.replace('FORMAT_EXAMPLE_PLACEHOLDER', example)
    return question

for row in data:
    question = format_prompt(row, add_context=False, format_example_group=1)
    answer = row['correct_answer']
    pair = {"question": question, "answer": answer}
    pairs.append(pair)

# CONTEXT_PLACEHOLDER
# FORMAT_EXAMPLE_PLACEHOLDER

# save the pairs to a json file
output_fn = "results/NousResearch_Meta-Llama-3-8B-Instruct_qa_pairs.json"
with open(output_fn, 'w') as outfile:
    json.dump(pairs, outfile, indent=4)
print(f"Saved {len(pairs)} question-answer pairs to {output_fn}")
