#!/usr/bin/env python3
"""
Test Simple Alpha-Beta vs Optimized Alpha-Beta
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chessapp.ai import SimpleAlphaBetaAI, AggressiveAlphaBetaAI
from chessapp.simulate import GameSimulator
from chessapp.engine import Board

def test_alpha_beta_comparison():
    """Test Simple vs Optimized Alpha-Beta configurations."""
    
    print("ALPHA-BETA vs ALPHA-BETA COMPARISON")
    print("=" * 50)
    print("Simple Config: Depth 3, no move ordering, basic evaluation")
    print("Optimized Config: Depth 4, move ordering, aggressive evaluation")
    print()
    
    simulator = GameSimulator()
    
    def simple_alpha_beta(board: Board):
        ai = SimpleAlphaBetaAI(depth=3, time_limit=2.0)
        return ai.get_move(board)
    
    def optimized_alpha_beta(board: Board):
        ai = AggressiveAlphaBetaAI(depth=4, time_limit=3.0)
        return ai.get_move(board)
    
    # Run the comparison
    results = simulator.simulate_match(
        white_ai=simple_alpha_beta,
        black_ai=optimized_alpha_beta,
        num_games=10,
        white_name="Simple Alpha-Beta (depth=3)",
        black_name="Optimized Alpha-Beta (depth=4)",
        verbose=False
    )
    
    print(f"\nKEY DIFFERENCES:")
    print(f"- Simple: Basic material evaluation, no move ordering")
    print(f"- Optimized: Aggressive evaluation, checkmate prioritization, move ordering")
    print(f"- Simple searches to depth 3, Optimized to depth 4")
    print(f"- Optimized should demonstrate superior play")
    
    print(f"\nRESULT ANALYSIS:")
    if results['black_win_rate'] > 0.6:
        print("✓ Optimized Alpha-Beta shows clear superiority")
    elif results['black_win_rate'] > 0.4:
        print("~ Optimized Alpha-Beta shows moderate advantage") 
    else:
        print("✗ Optimized Alpha-Beta needs improvement")
    
    return results

if __name__ == "__main__":
    test_alpha_beta_comparison()
