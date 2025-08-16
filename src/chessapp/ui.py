import pygame
from typing import Optional, Tuple
from .engine import Board, Move
from .ai import random_ai_move, AlphaBetaAI

SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
FONT_COLOR = (10, 10, 10)

PIECE_UNICODE = {
    "wK": "♔",
    "wQ": "♕",
    "wR": "♖",
    "wB": "♗",
    "wN": "♘",
    "wP": "♙",
    "bK": "♚",
    "bQ": "♛",
    "bR": "♜",
    "bB": "♝",
    "bN": "♞",
    "bP": "♟",
}


def draw_board(
    screen, board: Board, selected: Optional[Tuple[int, int]], legal_moves_for_selected
):
    font = pygame.font.SysFont("DejaVu Sans", 48)
    for r in range(8):
        for c in range(8):
            rect = pygame.Rect(
                c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
            )
            color = LIGHT_COLOR if (r + c) % 2 == 0 else DARK_COLOR
            if selected == (r, c):
                color = HIGHLIGHT
            pygame.draw.rect(screen, color, rect)
            piece = board.board[r][c]
            if piece:
                text = font.render(PIECE_UNICODE[piece], True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    # highlight legal destinations
    if selected:
        for mv in legal_moves_for_selected:
            if mv.start == selected:
                er, ec = mv.end
                center = (
                    ec * SQUARE_SIZE + SQUARE_SIZE // 2,
                    er * SQUARE_SIZE + SQUARE_SIZE // 2,
                )
                pygame.draw.circle(screen, (50, 150, 50), center, 10)


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess (Human vs Alpha-Beta AI)")
    clock = pygame.time.Clock()
    board = Board()

    selected: Optional[Tuple[int, int]] = None
    running = True
    
    # Create Alpha-Beta AI
    ai_engine = AlphaBetaAI(depth=4, use_move_ordering=True, time_limit=3.0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                r = my // SQUARE_SIZE
                c = mx // SQUARE_SIZE
                if selected is None:
                    # select piece if it belongs to human (white)
                    piece = board.board[r][c]
                    if piece and piece[0] == "w" and board.turn == "w":
                        selected = (r, c)
                else:
                    # attempt move
                    start = selected
                    move_made = False
                    for mv in board.generate_legal_moves():
                        if mv.start == start and mv.end == (r, c):
                            board.make_move(mv)
                            move_made = True
                            break
                    selected = None
                    if move_made:
                        # after human move, AI moves if game not over
                        if not board.result():
                            ai_move = ai_engine.get_move(board)
                            if ai_move:
                                board.make_move(ai_move)
                                print(f"AI played: {ai_move} (evaluated {ai_engine.nodes_evaluated:,} nodes)")
        screen.fill((0, 0, 0))
        legal_moves = list(board.generate_legal_moves())
        draw_board(screen, board, selected, legal_moves)
        if board.result():
            # display result overlay
            font = pygame.font.SysFont("DejaVu Sans", 40)
            result_text = board.result()
            surf = font.render(result_text, True, (200, 20, 20))
            rect = surf.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
            screen.blit(surf, rect)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
