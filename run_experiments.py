#!/usr/bin/env python3
"""
Milestone 2 Experiments Runner
Run the Alpha-Beta AI experiments required for Milestone 2
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chessapp.simulate import run_milestone2_experiments

if __name__ == "__main__":
    print("Starting Milestone 2 Experiments...")
    print("This will test the Alpha-Beta AI implementation.")
    print("Expected runtime: 2-5 minutes\n")
    
    try:
        results = run_milestone2_experiments()
        print("\nExperiments completed successfully!")
        print("Check the output above for detailed results and performance analysis.")
        
    except KeyboardInterrupt:
        print("\nExperiments interrupted by user.")
    except Exception as e:
        print(f"\nError running experiments: {e}")
        import traceback
        traceback.print_exc()
