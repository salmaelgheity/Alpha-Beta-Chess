#!/usr/bin/env python3
"""
Test improved Alpha-Beta with checkmate capability
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chessapp.ai import AlphaBetaAI, random_ai_move
from chessapp.engine import Board

def test_improved_alpha_beta():
    """Test the improved Alpha-Beta that should deliver checkmate."""
    board = Board()
    # Use improved Alpha-Beta with deeper search for winning positions
    alpha_beta = AlphaBetaAI(depth=4, use_move_ordering=True, time_limit=3.0)
    
    print("Testing IMPROVED Alpha-Beta vs Random AI")
    print("Should now deliver checkmate in winning positions")
    print("-" * 50)
    
    moves = 0
    max_moves = 150  # Reasonable limit for a proper game
    
    while moves < max_moves:
        # Check for natural game end
        result = board.result()
        if result:
            print(f"\nGame ended naturally: {result} after {moves} moves")
            if result == "1-0":
                print("✓ White (Alpha-Beta) won by checkmate!")
                return True
            elif result == "0-1":
                print("✗ Black (Random) won - very unexpected!")
                return False
            else:
                print("- Draw by stalemate/repetition")
                return False
        
        # Get move from current player
        if board.turn == 'w':
            move = alpha_beta.get_move(board)
            player = "Alpha-Beta"
        else:
            move = random_ai_move(board)
            player = "Random"
        
        if move and board.make_move(move):
            moves += 1
            if moves % 20 == 0:
                print(f"Move {moves}: {player} played {move}")
        else:
            print(f"{player} couldn't make a move")
            break
    
    # If we reach here, the game was too long
    print(f"\nGame reached {max_moves} moves without conclusion")
    
    # Check material to see who's winning
    white_material = 0
    black_material = 0
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece:
                value = piece_values[piece[1]]
                if piece[0] == 'w':
                    white_material += value
                else:
                    black_material += value
    
    print(f"Final material: White {white_material}, Black {black_material}")
    
    if white_material > black_material + 5:
        print("✓ Alpha-Beta achieved dominant material advantage")
        return True
    else:
        print("✗ Alpha-Beta did not achieve expected dominance")
        return False

if __name__ == "__main__":
    success = test_improved_alpha_beta()
    if success:
        print("\n✓ Test PASSED - Alpha-Beta shows clear superiority")
    else:
        print("\n✗ Test FAILED - Alpha-Beta needs more improvement")
