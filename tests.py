import sys, pathlib

sys.path.append(str(pathlib.Path(__file__).parent / "src"))
from chessapp.engine import Board, Move


def test_initial_legal_move_count():
    b = Board()
    moves = b.generate_legal_moves()
    # In initial position there are 20 legal moves
    assert len(moves) == 20, f"Expected 20 moves, got {len(moves)}"


def test_scholars_mate_result():
    b = Board()

    # Helper to fetch move by coordinate string produced by Move.__repr__
    def find(b, code):
        for mv in b.generate_legal_moves():
            if repr(mv) == code:
                return mv
        raise AssertionError(f"Move {code} not found among legal moves")

    # 1. e4 e5
    b.make_move(find(b, "e2e4"))
    b.make_move(find(b, "e7e5"))
    # 2. Qh5 Nc6
    b.make_move(find(b, "d1h5"))
    b.make_move(find(b, "b8c6"))
    # 3. Bc4 Nf6
    b.make_move(find(b, "f1c4"))
    b.make_move(find(b, "g8f6"))
    # 4. Qxf7# (represented as h5f7)
    b.make_move(find(b, "h5f7"))
    assert b.result() == "1-0", f"Expected 1-0 after Scholar's Mate, got {b.result()}"


if __name__ == "__main__":
    test_initial_legal_move_count()
    test_scholars_mate_result()
    print("All tests passed")
