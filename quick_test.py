#!/usr/bin/env python3
"""
Quick test to verify Alpha-Beta beats Random AI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chessapp.ai import AlphaBetaAI, random_ai_move
from chessapp.engine import Board
from chessapp.simulate import GameSimulator

def test_alpha_beta_vs_random():
    """Quick test to ensure Alpha-Beta beats Random consistently."""
    simulator = GameSimulator()
    
    def alpha_beta_player(board):
        ai = AlphaBetaAI(depth=3, use_move_ordering=True, time_limit=2.0)
        return ai.get_move(board)
    
    def random_player(board):
        return random_ai_move(board)
    
    print("Testing Alpha-Beta vs Random AI (5 games)...")
    print("Alpha-Beta should win all or almost all games.\n")
    
    results = simulator.simulate_match(
        white_ai=alpha_beta_player,
        black_ai=random_player,
        num_games=5,
        white_name="Alpha-Beta",
        black_name="Random",
        verbose=False
    )
    
    print(f"\nResult Summary:")
    print(f"Alpha-Beta win rate: {results['white_win_rate']:.1%}")
    print(f"Expected: >90% win rate")
    
    if results['white_win_rate'] >= 0.8:
        print("✓ PASSED: Alpha-Beta dominates Random AI")
    else:
        print("✗ FAILED: Alpha-Beta should win more consistently")
        
    return results

if __name__ == "__main__":
    test_alpha_beta_vs_random()
