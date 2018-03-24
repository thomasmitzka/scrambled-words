"""Tests for the module 'scrambled_words.py'

Use these tests to make sure the class methods work as expected.
"""

import unittest

from scrambled_words import ScrambledWords


class ScrambledWordsTestCase(unittest.TestCase):
    """A test case for the class ScrambledWords."""

    def setUp(self):
        """Create a class instance for all following tests."""
        self.sw = ScrambledWords()

    def test_get_words(self):
        """Are words read from the word file?"""
        self.assertTrue(self.sw.words)

    def test_scramble(self):
        """Are all scrambled words different than the original ones?"""
        self.assertTrue(self.sw.scrambled_words)
        for scrambled_word in self.sw.scrambled_words:
            self.assertNotIn(scrambled_word, self.sw.words)

    def test_create_hint(self):
        """Is the hint for a word created correctly?"""
        word = "apple"
        hint = self.sw.create_hint(word)
        self.assertEqual(word[:3], hint[:3])
        self.assertNotEqual(word[3:], hint[3:])

    def test_reset_game(self):
        """Are attributes reset when the user chooses to play again?"""
        self.sw.current_level = 1
        self.sw.reset_game()
        self.assertEqual(0, self.sw.current_level)

        words = self.sw.words
        self.sw.reset_game()
        self.assertNotEqual(words, self.sw.words)

        scrambled_words = self.sw.scrambled_words
        self.sw.scrambled_words = []
        self.sw.reset_game()
        self.assertNotEqual(scrambled_words, self.sw.scrambled_words)

        self.sw.level_times = [2.4, 13.0, 0]
        self.sw.reset_game()
        self.assertFalse(self.sw.level_times)

        self.sw.hint = False
        self.sw.reset_game()
        self.assertTrue(self.sw.hint)

    def test_reset_words(self):
        """Is the current level reset for a new game?"""
        self.sw.current_level = 1
        self.sw.reset_game()


unittest.main()
