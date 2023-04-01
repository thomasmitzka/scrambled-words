"""Use these tests to make sure the class methods work as expected."""

import pytest
from scrambled_words import ScrambledWords

@pytest.fixture
def sw():
    """Create an instance of ScrambledWords for all test functions."""
    sw = ScrambledWords()
    return sw

def test_get_words(sw):
    """Are words read from the word file?"""
    assert sw.words

def test_scramble(sw):
    """Are all scrambled words different than the original ones?"""
    assert sw.scrambled_words
    for scrambled_word in sw.scrambled_words:
        assert scrambled_word not in sw.words

def test_create_hint(sw):
    """Is the hint for a word created correctly?"""
    word = "apple"
    hint = sw.create_hint(word)
    assert word[:3] == hint[:3]
    assert word[3:] != hint[3:]

def test_reset_game(sw):
    """Are attributes reset when the user chooses to play again?"""
    # Test reset of current level number.
    sw.current_level = 1
    sw.reset_game()
    assert sw.current_level == 0

    # Test reset of word list.
    # There is a slight chance that the same list is created again.
    words = sw.words
    sw.reset_game()
    assert words != sw.words

    # Test reset of scrambled word list.
    # There is a slight chance that the same list is created again.
    scrambled_words = sw.scrambled_words
    sw.reset_game()
    assert scrambled_words != sw.scrambled_words

    # Test reset of level times.
    sw.level_times = [2.4, 13.0, 0]
    sw.reset_game()
    assert not sw.level_times

    # Test reset of hint flag.
    sw.hint = False
    sw.reset_game()
    assert sw.hint
