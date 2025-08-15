import random
from .engine import Board, Move


def random_ai_move(board: Board) -> Move | None:
    moves = board.generate_legal_moves()
    if not moves:
        return None
    return random.choice(moves)
