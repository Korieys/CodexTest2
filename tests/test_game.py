import pytest

from vodle.game import VodleError, VodleGame


def test_exact_match_wins_in_one_attempt():
    game = VodleGame("vivid", max_attempts=6)
    result = game.evaluate_guess("vivid")

    assert result.is_correct is True
    assert game.has_won is True
    assert game.is_over is True
    assert game.remaining_attempts == 5


def test_repeated_letters_are_scored_correctly():
    game = VodleGame("vivid", max_attempts=3)
    result = game.evaluate_guess("divvy")
    statuses = [hint.status for hint in result.hints]

    # d is present, i is correct, v is correct, the second v is present once, y is absent
    assert statuses == ["present", "correct", "correct", "present", "absent"]


def test_invalid_guess_length_raises():
    game = VodleGame("vivid", max_attempts=3)
    with pytest.raises(VodleError):
        game.evaluate_guess("too-long")


def test_game_tracks_remaining_attempts_and_end_state():
    game = VodleGame("vivid", max_attempts=2)
    game.evaluate_guess("vexed")
    game.evaluate_guess("vexed")

    assert game.is_over is True
    assert game.has_won is False
    assert game.remaining_attempts == 0
