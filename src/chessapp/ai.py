import random
import time
from typing import Dict, List, Tuple, Optional
from .engine import Board, Move, WHITE, BLACK


def random_ai_move(board: Board) -> Move | None:
    """Random AI that selects a random legal move."""
    moves = board.generate_legal_moves()
    if not moves:
        return None
    return random.choice(moves)


class AggressiveAlphaBetaAI:
    """Aggressive Alpha-Beta AI that prioritizes winning and delivering checkmate."""
    
    def __init__(self, depth: int = 4, time_limit: float = 3.0):
        self.max_depth = depth
        self.time_limit = time_limit
        self.nodes_evaluated = 0
        self.start_time = 0.0
        
        # Piece values - slightly higher for active pieces
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000
        }

    def get_move(self, board: Board) -> Move | None:
        """Get the best move using Alpha-Beta pruning."""
        self.nodes_evaluated = 0
        self.start_time = time.time()
        
        legal_moves = board.generate_legal_moves()
        if not legal_moves:
            return None
            
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        best_move = legal_moves[0]
        best_score = float('-inf')
        
        # Order moves to try the most promising first
        ordered_moves = self.order_moves(board, legal_moves)
        
        alpha = float('-inf')
        beta = float('inf')
        
        for move in ordered_moves:
            if time.time() - self.start_time > self.time_limit:
                break
                
            clone = board.clone()
            clone._apply_move(move)
            
            score = -self.alpha_beta(clone, self.max_depth - 1, -beta, -alpha, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, score)
                
        return best_move

    def alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, 
                   maximizing_player: bool) -> float:
        """Alpha-Beta pruning algorithm."""
        self.nodes_evaluated += 1
        
        if time.time() - self.start_time > self.time_limit:
            return 0  # Time's up
        
        # Check for game end
        result = board.result()
        if result is not None:
            if result == "1-0":  # White wins
                return 10000 - (self.max_depth - depth) if maximizing_player else -10000 + (self.max_depth - depth)
            elif result == "0-1":  # Black wins
                return -10000 + (self.max_depth - depth) if maximizing_player else 10000 - (self.max_depth - depth)
            else:  # Draw
                return 0
        
        if depth <= 0:
            return self.evaluate_position(board)
        
        moves = board.generate_legal_moves()
        if not moves:
            # Should have been caught by result() but just in case
            if board.is_in_check(board.turn):
                return -10000 + (self.max_depth - depth)  # Checkmate
            return 0  # Stalemate
        
        # Order moves for better pruning
        moves = self.order_moves(board, moves)
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                clone = board.clone()
                clone._apply_move(move)
                eval_score = self.alpha_beta(clone, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                clone = board.clone()
                clone._apply_move(move)
                eval_score = self.alpha_beta(clone, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return min_eval

    def evaluate_position(self, board: Board) -> float:
        """Aggressive evaluation that prioritizes winning."""
        white_material = 0
        black_material = 0
        
        # Count material and look for winning opportunities
        for r in range(8):
            for c in range(8):
                piece = board.board[r][c]
                if piece:
                    value = self.piece_values[piece[1]]
                    if piece[0] == WHITE:
                        white_material += value
                    else:
                        black_material += value
        
        score = white_material - black_material
        
        # If we have a big material advantage, be very aggressive
        material_diff = abs(white_material - black_material)
        if material_diff > 500:  # Significant advantage
            # Encourage attacking the enemy king
            enemy_color = BLACK if board.turn == WHITE else WHITE
            try:
                enemy_king_pos = board.king_position(enemy_color)
                my_king_pos = board.king_position(board.turn)
                
                # Bonus for getting closer to enemy king when winning
                king_distance = abs(my_king_pos[0] - enemy_king_pos[0]) + abs(my_king_pos[1] - enemy_king_pos[1])
                
                # Drive enemy king to edges
                edge_distance = min(enemy_king_pos[0], 7 - enemy_king_pos[0], 
                                  enemy_king_pos[1], 7 - enemy_king_pos[1])
                
                # Aggressive bonuses when we're winning
                if (board.turn == WHITE and white_material > black_material) or \
                   (board.turn == BLACK and black_material > white_material):
                    score += (10 - king_distance) * 30  # Get closer to enemy king
                    score += (4 - edge_distance) * 50   # Drive to edge
                    
                    # Extra bonus for having queens near enemy king
                    for r in range(8):
                        for c in range(8):
                            piece = board.board[r][c]
                            if piece and piece[0] == board.turn and piece[1] == 'Q':
                                queen_distance = abs(r - enemy_king_pos[0]) + abs(c - enemy_king_pos[1])
                                score += (8 - queen_distance) * 40
                                
            except:
                pass  # If king position lookup fails
        
        # Mobility bonus
        num_moves = len(board.generate_legal_moves())
        score += num_moves * 5
        
        return score

    def order_moves(self, board: Board, moves: List[Move]) -> List[Move]:
        """Order moves to try the most promising first."""
        def move_score(move: Move) -> float:
            score = 0
            
            # Prioritize captures
            captured = board.piece_at(move.end)
            if captured:
                score += self.piece_values[captured[1]] * 10
                
            # Prioritize promotions
            if move.promotion:
                score += 800
                
            # Check if move gives check
            clone = board.clone()
            try:
                clone._apply_move(move)
                if clone.is_in_check(clone.turn):
                    score += 100
                    
                    # Massive bonus if it's checkmate
                    if not clone.generate_legal_moves():
                        score += 50000
                        
            except:
                pass
                
            return score
        
        return sorted(moves, key=move_score, reverse=True)


# Convenience function
def alpha_beta_ai_move(board: Board, depth: int = 4) -> Move | None:
    """Get move from aggressive Alpha-Beta AI."""
    ai = AggressiveAlphaBetaAI(depth=depth, time_limit=3.0)
    return ai.get_move(board)
