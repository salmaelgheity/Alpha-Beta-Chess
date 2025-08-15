# Simple Chess (Human vs Random AI)

A lightweight chess application built with Python and Pygame. Human plays White against a random-move AI controlling Black.

## Features

- Full 8x8 chessboard rendering using Unicode symbols
- Legal move generation with: moves, captures, promotions, en-passant, castling (basic legality)
- Check, checkmate, stalemate detection
- Random AI opponent

## Requirements

Install dependencies:

```
pip install -r requirements.txt
```

## Run

```
python -m src.main
```

(Or run `python src/main.py`.)

## Controls

- Left click a white piece to select.
- Left click a destination square (highlighted dots show legal targets for the selected piece).
- Game result displayed when finished (1-0, 0-1, or 1/2-1/2).

## Notes / Simplifications

- Castling legality only filtered finally by king-in-check test (doesn't yet forbid castling through check squares explicitly, but resulting illegal positions are filtered by standard check test after move). This could allow transiently illegal castle if squares attacked; improvement left as future enhancement.
- No draw claims by repetition or 50-move rule.

## Next Steps Ideas

- Add minimax / material evaluation AI
- Add move history panel & PGN export
- Add threefold repetition and 50-move rule
- Add per-piece sprite graphics

Enjoy!
