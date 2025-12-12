"""Command-line interface for playing Vodle."""

from __future__ import annotations

import argparse
import sys
from typing import Iterable

from .game import VodleError, VodleGame
from .words import is_valid_guess, pick_random_word

STATUS_TO_EMOJI = {
    "correct": "🟩",
    "present": "🟨",
    "absent": "⬜",
}


def format_feedback(result) -> str:
    return " ".join(f"{STATUS_TO_EMOJI[hint.status]} {hint.letter.upper()}" for hint in result.hints)


def prompt_for_guess(length: int) -> str:
    while True:
        guess = input(f"Enter a {length}-letter guess (or 'quit'): ").strip().lower()
        if guess in {"quit", "exit"}:
            raise SystemExit(0)
        if is_valid_guess(guess, length=length):
            return guess
        print("Please enter letters only, matching the required length.")


def run_game(length: int, max_attempts: int, *, seed: int | None = None) -> int:
    secret = pick_random_word(length, seed=seed)
    game = VodleGame(secret, max_attempts=max_attempts)

    print("Welcome to Vodle! Guess the secret word before you run out of attempts.")
    print(f"The secret word has {length} letters. You have {max_attempts} attempts.\n")

    while not game.is_over:
        print(f"Attempts remaining: {game.remaining_attempts}")
        guess = prompt_for_guess(length)
        try:
            result = game.evaluate_guess(guess)
        except VodleError as exc:
            print(exc)
            continue

        print(format_feedback(result))
        print()

        if result.is_correct:
            print(f"🎉 Correct! The Vodle was '{secret}'.")
            return 0

    print(f"Out of attempts. The Vodle was '{secret}'. Better luck next time!")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Play Vodle in your terminal.")
    parser.add_argument("--length", type=int, default=5, help="Length of the secret word (default: 5)")
    parser.add_argument("--attempts", type=int, default=6, help="Maximum guesses allowed (default: 6)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible puzzles")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return run_game(args.length, args.attempts, seed=args.seed)
    except ValueError as exc:
        print(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
