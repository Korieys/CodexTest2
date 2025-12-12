"""Word list utilities for the Vodle game."""

from __future__ import annotations

import random
from typing import List

# A small curated list of approachable words so the game is fun in a terminal.
WORDS: List[str] = [
    "vivid",
    "vogue",
    "viper",
    "value",
    "vowel",
    "vital",
    "vouch",
    "visor",
    "vivid",
    "vexed",
    "venom",
    "viper",
    "vodka",
    "voice",
    "vocal",
    "voted",
    "vivid",
    "vines",
    "vogue",
    "vouch",
    "vista",
    "vinyl",
    "vault",
    "vials",
    "vroom",
    "valor",
    "vividly",
    "voyage",
    "velvet",
    "viable",
    "vector",
    "victor",
    "vacuum",
    "varied",
    "visual",
]


def words_of_length(length: int) -> List[str]:
    """Return all allowed words matching ``length``.

    The function quietly ignores any length shorter than three to avoid
    accidental zero-length games.
    """

    if length < 3:
        return []
    return [word for word in WORDS if len(word) == length]


def pick_random_word(length: int, *, seed: int | None = None) -> str:
    """Pick a random word of a given length.

    Args:
        length: Number of letters the word should contain.
        seed: Optional random seed for reproducible sessions.

    Raises:
        ValueError: If there is no word matching the requested length.
    """

    available = words_of_length(length)
    if not available:
        raise ValueError(f"No words available for length {length}.")
    rng = random.Random(seed)
    return rng.choice(available)


def is_valid_guess(word: str, *, length: int) -> bool:
    """Return whether ``word`` is a plausible guess for the given length."""

    return word.isalpha() and len(word) == length
