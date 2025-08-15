from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterable

# Basic piece representations
WHITE = "w"
BLACK = "b"
PIECES = {"P", "N", "B", "R", "Q", "K"}


@dataclass(frozen=True)
class Move:
    start: Tuple[int, int]
    end: Tuple[int, int]
    promotion: Optional[str] = None

    def __repr__(self) -> str:
        sfile = chr(self.start[1] + ord("a"))
        srank = 8 - self.start[0]
        efile = chr(self.end[1] + ord("a"))
        erank = 8 - self.end[0]
        promo = f"={self.promotion}" if self.promotion else ""
        return f"{sfile}{srank}{efile}{erank}{promo}"


class Board:
    def __init__(self):
        # board[r][c], r=0 top (8th rank), c=0 left (file a)
        self.board: List[List[Optional[str]]] = [[None] * 8 for _ in range(8)]
        self.turn: str = WHITE
        self.history: List[Tuple[Move, Optional[str], Optional[str]]] = (
            []
        )  # move, captured, castling_rights snapshot
        self.castling_rights = {"K": True, "Q": True, "k": True, "q": True}
        self.en_passant: Optional[Tuple[int, int]] = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self._setup()

    def _setup(self):
        # Setup initial position
        pieces_back = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        self.board[0] = [f"b{p}" for p in pieces_back]
        self.board[1] = ["bP"] * 8
        self.board[6] = ["wP"] * 8
        self.board[7] = [f"w{p}" for p in pieces_back]

    def clone(self) -> "Board":
        import copy

        b = Board.__new__(Board)  # bypass init
        b.board = copy.deepcopy(self.board)
        b.turn = self.turn
        b.history = list(self.history)
        b.castling_rights = dict(self.castling_rights)
        b.en_passant = self.en_passant
        b.halfmove_clock = self.halfmove_clock
        b.fullmove_number = self.fullmove_number
        return b

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def piece_at(self, sq: Tuple[int, int]):
        r, c = sq
        return self.board[r][c]

    def is_white(self, piece: str):
        return piece.startswith("w")

    def is_black(self, piece: str):
        return piece.startswith("b")

    def king_position(self, color: str) -> Tuple[int, int]:
        target = f"{color}K"
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r, c)
        raise ValueError("King missing")

    def generate_legal_moves(self) -> List[Move]:
        moves = []
        for mv in self.generate_pseudo_legal_moves():
            if self._is_legal(mv):
                moves.append(mv)
        return moves

    def _is_legal(self, move: Move) -> bool:
        clone = self.clone()
        clone._apply_move(move)
        return not clone.is_in_check(self.turn)

    def is_in_check(self, color: str) -> bool:
        king_sq = self.king_position(color)
        return self._square_attacked(king_sq, WHITE if color == BLACK else BLACK)

    def _square_attacked(self, sq: Tuple[int, int], by_color: str) -> bool:
        # brute force: generate all pseudo moves of opponent and see if any end square matches
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == by_color:
                    for mv in self._piece_moves((r, c), piece, attacks_only=True):
                        if mv.end == sq:
                            return True
        return False

    def generate_pseudo_legal_moves(self) -> Iterable[Move]:
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == self.turn:
                    yield from self._piece_moves((r, c), piece)

    def _piece_moves(
        self, sq: Tuple[int, int], piece: str, attacks_only=False
    ) -> Iterable[Move]:
        color = piece[0]
        kind = piece[1]
        r, c = sq
        forward = -1 if color == WHITE else 1
        enemy = BLACK if color == WHITE else WHITE
        if kind == "P":
            # single push
            nr = r + forward
            if self.in_bounds(nr, c) and not attacks_only and self.board[nr][c] is None:
                # promotion check
                if nr == 0 or nr == 7:
                    for promo in ["Q", "R", "B", "N"]:
                        yield Move((r, c), (nr, c), promo)
                else:
                    yield Move((r, c), (nr, c))
                # double push
                start_rank = 6 if color == WHITE else 1
                if r == start_rank:
                    nnr = r + 2 * forward
                    if self.board[nnr][c] is None:
                        yield Move((r, c), (nnr, c))
            # captures
            for dc in (-1, 1):
                nr, nc = r + forward, c + dc
                if self.in_bounds(nr, nc):
                    target = self.board[nr][nc]
                    if target and target[0] == enemy:
                        if nr == 0 or nr == 7:
                            for promo in ["Q", "R", "B", "N"]:
                                yield Move((r, c), (nr, nc), promo)
                        else:
                            yield Move((r, c), (nr, nc))
                    # en passant
                    if self.en_passant == (nr, nc):
                        yield Move((r, c), (nr, nc))
        elif kind in ("N", "K"):
            deltas = []
            if kind == "N":
                deltas = [
                    (2, 1),
                    (1, 2),
                    (-1, 2),
                    (-2, 1),
                    (-2, -1),
                    (-1, -2),
                    (1, -2),
                    (2, -1),
                ]
            else:
                deltas = [
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 1),
                    (-1, 0),
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                ]
            for dr, dc in deltas:
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    target = self.board[nr][nc]
                    if target is None or target[0] == enemy:
                        yield Move((r, c), (nr, nc))
            if kind == "K" and not attacks_only:
                # Castling (very simplified: ignore squares attacked check for brevity except final legality filter)
                if color == WHITE:
                    rank = 7
                    if (
                        self.castling_rights["K"]
                        and self.board[7][5] is None
                        and self.board[7][6] is None
                    ):
                        yield Move((7, 4), (7, 6))
                    if (
                        self.castling_rights["Q"]
                        and self.board[7][3] is None
                        and self.board[7][2] is None
                        and self.board[7][1] is None
                    ):
                        yield Move((7, 4), (7, 2))
                else:
                    rank = 0
                    if (
                        self.castling_rights["k"]
                        and self.board[0][5] is None
                        and self.board[0][6] is None
                    ):
                        yield Move((0, 4), (0, 6))
                    if (
                        self.castling_rights["q"]
                        and self.board[0][3] is None
                        and self.board[0][2] is None
                        and self.board[0][1] is None
                    ):
                        yield Move((0, 4), (0, 2))
        else:
            directions = []
            if kind == "B":
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            elif kind == "R":
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            elif kind == "Q":
                directions = [
                    (1, 1),
                    (1, -1),
                    (-1, 1),
                    (-1, -1),
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                ]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while self.in_bounds(nr, nc):
                    target = self.board[nr][nc]
                    if target is None:
                        yield Move((r, c), (nr, nc))
                    else:
                        if target[0] == enemy:
                            yield Move((r, c), (nr, nc))
                        break
                    nr += dr
                    nc += dc

    def _apply_move(self, move: Move):
        sr, sc = move.start
        er, ec = move.end
        piece = self.board[sr][sc]
        captured = self.board[er][ec]
        # en passant capture
        if (
            piece
            and piece[1] == "P"
            and self.en_passant == (er, ec)
            and captured is None
        ):
            # captured pawn is behind target square
            direction = 1 if piece[0] == WHITE else -1
            self.board[er - direction][ec] = None
            captured = f"{('b' if piece[0]==WHITE else 'w')}P"
        # move piece
        self.board[er][ec] = piece
        self.board[sr][sc] = None
        # promotion
        if piece and piece[1] == "P" and move.promotion:
            self.board[er][ec] = piece[0] + move.promotion
        # castling rook move
        if piece and piece[1] == "K" and abs(ec - sc) == 2:
            if ec == 6:  # king side
                self.board[er][5] = self.board[er][7]
                self.board[er][7] = None
            else:  # queen side
                self.board[er][3] = self.board[er][0]
                self.board[er][0] = None
        # update en-passant square
        self.en_passant = None
        if piece and piece[1] == "P" and abs(er - sr) == 2:
            self.en_passant = ((er + sr) // 2, ec)
        # update castling rights if rooks/king moved or captured
        if piece == "wK":
            self.castling_rights["K"] = False
            self.castling_rights["Q"] = False
        if piece == "bK":
            self.castling_rights["k"] = False
            self.castling_rights["q"] = False
        if piece == "wR" and sr == 7 and sc == 0:
            self.castling_rights["Q"] = False
        if piece == "wR" and sr == 7 and sc == 7:
            self.castling_rights["K"] = False
        if piece == "bR" and sr == 0 and sc == 0:
            self.castling_rights["q"] = False
        if piece == "bR" and sr == 0 and sc == 7:
            self.castling_rights["k"] = False
        if captured == "wR" and er == 7 and ec == 0:
            self.castling_rights["Q"] = False
        if captured == "wR" and er == 7 and ec == 7:
            self.castling_rights["K"] = False
        if captured == "bR" and er == 0 and ec == 0:
            self.castling_rights["q"] = False
        if captured == "bR" and er == 0 and ec == 7:
            self.castling_rights["k"] = False
        # half/full move counters
        if piece and piece[1] == "P" or captured:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        if self.turn == BLACK:
            self.fullmove_number += 1
        # switch turn
        self.turn = BLACK if self.turn == WHITE else WHITE
        self.history.append((move, captured, None))

    def make_move(self, move: Move) -> bool:
        if move in self.generate_legal_moves():
            self._apply_move(move)
            return True
        return False

    def is_checkmate(self) -> bool:
        # Side to move has no legal moves AND is in check
        if self.generate_legal_moves():
            return False
        return self.is_in_check(self.turn)

    def is_stalemate(self) -> bool:
        # Side to move has no legal moves AND is NOT in check
        if self.generate_legal_moves():
            return False
        return not self.is_in_check(self.turn)

    def result(self) -> Optional[str]:
        # Determine game result in standard chess notation.
        # Return '1-0' if White wins, '0-1' if Black wins, '1/2-1/2' for draw, or None if ongoing.
        legal = self.generate_legal_moves()
        if legal:
            return None
        if self.is_in_check(self.turn):
            # Side to move is checkmated; opponent wins.
            return "1-0" if self.turn == BLACK else "0-1"
        return "1/2-1/2"
