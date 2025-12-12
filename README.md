# Vodle

Vodle is a tiny, terminal-friendly word deduction game. Guess the hidden word within a limited number of attempts and get per-letter hints along the way.

## Quick start

```bash
python -m pip install -e .
vodle --length 5 --attempts 6
```

If you prefer not to install, you can also run it directly:

```bash
python -m vodle.cli --length 6 --attempts 7 --seed 42
```

### Gameplay
- Each letter in your guess is marked as:
  - 🟩 correct and in the right spot
  - 🟨 present elsewhere in the word
  - ⬜ not in the secret word
- You can type `quit` or `exit` to leave at any time.

## Development

Run the test suite with:

```bash
pytest
```

The code lives under `vodle/`, with gameplay logic in `game.py` and the command-line interface in `cli.py`.
