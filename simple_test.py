#!/usr/bin/env python3
"""
Simple test: Alpha-Beta vs Random without move limits
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chessapp.ai import AlphaBetaAI, random_ai_move
from chessapp.engine import Board

def test_single_game():
    """Test a single game between Alpha-Beta and Random AI."""
    board = Board()
    alpha_beta = AlphaBetaAI(depth=3, use_move_ordering=True, time_limit=2.0)
    
    print("Testing Alpha-Beta vs Random AI (single game)")
    print("No artificial move limits - let the game end naturally")
    print("-" * 50)
    
    moves = 0
    while True:
        # Check for natural game end
        result = board.result()
        if result:
            print(f"\nGame ended naturally: {result} after {moves} moves")
            if result == "1-0":
                print("✓ White (Alpha-Beta) won!")
            elif result == "0-1":
                print("✗ Black (Random) won - unexpected!")
            else:
                print("- Draw")
            return result
        
        # Get move from current player
        if board.turn == 'w':
            move = alpha_beta.get_move(board)
            player = "Alpha-Beta"
        else:
            move = random_ai_move(board)
            player = "Random"
        
        if move and board.make_move(move):
            moves += 1
            print(f"Move {moves}: {player} played {move}")
            
            # Safety check for very long games (but much higher limit)
            if moves > 500:
                print("Game is unusually long, stopping...")
                break
        else:
            print(f"{player} couldn't make a move")
            break
    
    return None

if __name__ == "__main__":
    test_single_game()
