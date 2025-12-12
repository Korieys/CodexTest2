"""Core Vodle game logic."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import List, Sequence


class VodleError(Exception):
    """Base exception raised by the Vodle package."""


@dataclass
class LetterHint:
    letter: str
    status: str  # "correct", "present", or "absent"

    def __post_init__(self) -> None:
        self.letter = self.letter.lower()


@dataclass
class GuessResult:
    """Represents the feedback for a single guess."""

    guess: str
    hints: List[LetterHint]

    @property
    def is_correct(self) -> bool:
        return all(h.status == "correct" for h in self.hints)


class VodleGame:
    """Encapsulates Vodle gameplay."""

    def __init__(self, secret_word: str, *, max_attempts: int = 6) -> None:
        if max_attempts < 1:
            raise VodleError("max_attempts must be at least 1")
        if not secret_word.isalpha():
            raise VodleError("The secret word must be alphabetic.")
        self.secret_word = secret_word.lower()
        self.max_attempts = max_attempts
        self.attempts: List[GuessResult] = []

    @property
    def remaining_attempts(self) -> int:
        return self.max_attempts - len(self.attempts)

    @property
    def is_over(self) -> bool:
        return self.remaining_attempts == 0 or any(a.is_correct for a in self.attempts)

    @property
    def has_won(self) -> bool:
        return any(a.is_correct for a in self.attempts)

    @property
    def history(self) -> Sequence[GuessResult]:
        return tuple(self.attempts)

    def evaluate_guess(self, guess: str) -> GuessResult:
        """Score a guess and record it in the history."""

        if self.is_over:
            raise VodleError("No attempts remaining.")
        if len(guess) != len(self.secret_word):
            raise VodleError("Incorrect word length.")
        if not guess.isalpha():
            raise VodleError("Guesses must be alphabetic.")

        guess = guess.lower()
        hints = _score_guess(self.secret_word, guess)
        result = GuessResult(guess=guess, hints=hints)
        self.attempts.append(result)
        return result


def _score_guess(secret: str, guess: str) -> List[LetterHint]:
    """Return per-letter hints for the guess compared to the secret word."""

    hints = [LetterHint(letter, "absent") for letter in guess]
    remaining_letters = Counter()

    # First pass: mark correct positions and collect remaining letters.
    for idx, (secret_letter, guess_letter) in enumerate(zip(secret, guess)):
        if guess_letter == secret_letter:
            hints[idx].status = "correct"
        else:
            remaining_letters[secret_letter] += 1

    # Second pass: mark letters that are present elsewhere.
    for idx, guess_letter in enumerate(guess):
        if hints[idx].status == "correct":
            continue
        if remaining_letters[guess_letter] > 0:
            hints[idx].status = "present"
            remaining_letters[guess_letter] -= 1

    return hints
