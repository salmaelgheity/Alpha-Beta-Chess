#!/usr/bin/env python3
"""
Test the aggressive Alpha-Beta vs Random
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chessapp.ai import AggressiveAlphaBetaAI, random_ai_move
from chessapp.engine import Board

def test_aggressive_match():
    """Test multiple games of Aggressive Alpha-Beta vs Random."""
    print("Testing Aggressive Alpha-Beta vs Random AI")
    print("=" * 50)
    
    wins = 0
    draws = 0
    losses = 0
    
    for game_num in range(5):
        print(f"\nGame {game_num + 1}:")
        
        board = Board()
        alpha_beta = AggressiveAlphaBetaAI(depth=4, time_limit=3.0)
        
        moves = 0
        max_moves = 150
        
        while moves < max_moves:
            result = board.result()
            if result:
                print(f"  Result: {result} after {moves} moves")
                if result == "1-0":
                    wins += 1
                    print("  ✓ Alpha-Beta won!")
                elif result == "0-1":
                    losses += 1
                    print("  ✗ Random won!")
                else:
                    draws += 1
                    print("  - Draw")
                break
            
            # Make moves
            if board.turn == 'w':
                move = alpha_beta.get_move(board)
                player = "Alpha-Beta"
            else:
                move = random_ai_move(board)
                player = "Random"
            
            if move and board.make_move(move):
                moves += 1
            else:
                print(f"  {player} failed to move")
                break
        else:
            # Game reached move limit - check material
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
            
            print(f"  Reached {max_moves} moves. Material: White {white_material}, Black {black_material}")
            
            if white_material > black_material + 2:
                wins += 1
                print("  ✓ Alpha-Beta won by material advantage!")
            elif black_material > white_material + 2:
                losses += 1
                print("  ✗ Random won by material advantage!")
            else:
                draws += 1
                print("  - Draw by material")
    
    print(f"\nFinal Results:")
    print(f"Alpha-Beta wins: {wins}/5 ({wins/5:.1%})")
    print(f"Draws: {draws}/5 ({draws/5:.1%})")
    print(f"Random wins: {losses}/5 ({losses/5:.1%})")
    
    if wins >= 4:
        print("\n✓ SUCCESS: Alpha-Beta dominates Random AI!")
        return True
    elif wins >= 3:
        print("\n~ PARTIAL: Alpha-Beta shows clear advantage")
        return True
    else:
        print("\n✗ FAILED: Alpha-Beta should win more consistently")
        return False

if __name__ == "__main__":
    test_aggressive_match()
