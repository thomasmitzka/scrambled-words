#!/usr/bin/env python3

"""Scrambled Words is a text-based word guessing game.

For further information on this game and how to play it, please read the
included file 'README.md'. By default, playing instructions are shown at
the beginning. You can change the game by altering the options at the
bottom of this module.
"""

import random
import time
import json


class ScrambledWords():
    """The main class of the game.

    It provides methods to read and scramble words, ask for user input,
    create a hint, read and show highscores, add new highscores and
    write them to file.
    """

    def __init__(self):
        """Initialize class variables.

        Call methods get_words() and scramble() for the first time to
        create a list of scrambled words. The number of levels depends
        on the number of lines in the word file.
        """
        self.words = self.get_words()
        if self.words:
            self.scrambled_words = self.scramble()
            self.total_levels = len(self.words)
        self.current_level = 0
        self.level_times = []
        self.hint = True
        self.continue_game = True

    def __repr__(self):
        """Provide information on this class."""
        return "Scrambled Words is a text-based word guessing game."

    @staticmethod
    def get_words():
        """Read words from file and return a list of random words.

        The list contains one word for each level.
        """
        try:
            with open(WORD_FILE, "r") as word_file:
                word_lists = [line.strip().split(",") for line in word_file]
        except FileNotFoundError:
            return None
        else:
            words = [random.choice(w_list).upper() for w_list in word_lists]
            return words

    def scramble(self):
        """Scramble words in list, and return list."""
        scrambled_words = []
        for word in self.words:
            scrambled_word = word
            # Make sure that the letter order is shuffled.
            while scrambled_word == word:
                letters = list(scrambled_word)
                random.shuffle(letters)
                scrambled_word = "".join(letters)
            scrambled_words.append(scrambled_word)
        return scrambled_words

    def next_level(self):
        """Raise level counter and start countdown to next level."""
        self.current_level += 1
        print("Get ready for level {} ...".format(self.current_level))
        time.sleep(4)

    def challenge(self):
        """Show scrambled word, take user input, and measure time.

        End level if the word has been solved or if guess limit has
        been reached. The hint option is not available if the word has
        less than five letters, because create_hint() corrects the
        first three letters.
        """
        scrambled_word = self.scrambled_words[self.current_level - 1]
        word = self.words[self.current_level - 1]
        guesses = MAX_GUESSES

        # Save start time.
        start = time.time()

        print("\n== Level {} of {} ({} points) ==".format(
            self.current_level, self.total_levels, self.current_level * 10
        ))

        user_input = ""
        while (user_input != word) and (guesses > 0):
            print("\n{}".format(scrambled_word))
            print("Remaining guesses: {}".format(guesses))

            user_input = input("> ").upper()

            if user_input == "H":
                if self.hint:
                    if len(word) > 4:
                        scrambled_word = self.create_hint(word)
                        self.hint = False
                        print("You requested a hint. Here it comes:")
                    else:
                        print("This word is too short to use the hint option.")
                        print("Try to unscramble it on your own.")
                else:
                    print("You already had one hint in this game.")
            elif user_input != word:
                guesses -= 1
                if guesses:
                    print("\nTry again.")

        print("\nThe word was: {}".format(word))

        if user_input == word:
            # Save finish and level time.
            finish = time.time()
            self.level_times.append(round((finish - start), 1))

            print(random.choice(("Well done!", "Great!", "Awesome!")), end=" ")
            print("You finished this level in {} seconds.".format(
                self.level_times[-1]
            ))
        else:
            self.level_times.append(0)
            print("You didn't guess this one.")

    @staticmethod
    def create_hint(word):
        """Create and return new string as a hint.

        Take the correct word as argument. Keep the first three letters,
        and shuffle the rest.
        """
        letters = list(word)
        part1 = letters[:3]
        part2 = letters[3:]
        # Make sure that the letter order is shuffled.
        while part2 == letters[3:]:
            random.shuffle(part2)
        return "".join(part1) + "".join(part2)

    def get_score(self):
        """Calculate regular and bonus points per level, and the total score.

        A level time of 0 means that the word was not solved. Each
        solved word is worth 10 times its level number. Double that
        amount if the level time doesn't exceed the time limit.
        """
        level_points = []
        level_bonus = []
        score = 0

        for i in range(self.total_levels):
            if self.level_times[i]:
                level_points.append((i + 1) * 10)

                if self.level_times[i] <= TIME_LIMIT:
                    level_bonus.append((i + 1) * 10)
                else:
                    level_bonus.append(0)

            else:
                level_points.append(0)
                level_bonus.append(0)

        for amount in level_points:
            score += amount
        for amount in level_bonus:
            score += amount
        return level_points, level_bonus, score

    def show_results(self, level_points, level_bonus, score):
        """Show the player's results."""
        time.sleep(4)
        print("\n== Results: ==")
        print("\nLvl\tPts\tBonus\tTime (sec)")
        for i in range(self.total_levels):
            print("{}\t{}\t{}\t".format(
                i + 1, level_points[i], level_bonus[i]), end=""
                 )
            if self.level_times[i] > 0:
                print(self.level_times[i])
            else:
                print("-")
        print("\nYour total score: {}".format(score))

    @staticmethod
    def get_highscores():
        """Read highscores from file and show them.

        If a new highscore has been achieved, save the player's name
        and score by calling method add_highscore(). Highscores are
        stored in a JSON file. There can only be 10 highscore entries
        at a time. A new highscore must at least be as high as the
        lowest (= last) entry in the list.
        """
        try:
            with open("highscores.json", "r") as hscore_file:
                scorelist = json.load(hscore_file)

                # Convert score numbers from string to integer,
                # so they can be compared and sorted.
                converted_scorelist = []
                for entry in scorelist:
                    points, player = entry
                    converted_scorelist.append([int(points), player])
                scorelist = converted_scorelist
        except FileNotFoundError:
            scorelist = []
        return scorelist

    @staticmethod
    def add_highscore(score, scorelist):
        """Add a new highscore, write list to file, and return list.

        If the list already contains ten or more highscore entries,
        remove the last entries before adding the new one. Sort the
        list before writing and returning it.
        """
        print("\n** NEW HIGHSCORE **")
        print("Please enter your name:")
        player = ""
        while player == "":
            player = input("> ")
        print("\nCongratulations, {}!".format(player))

        while len(scorelist) >= 10:
            scorelist.pop()

        scorelist.append([score, player])
        scorelist = sorted(scorelist, reverse=True)

        # Convert score numbers from integer to string,
        # so they can be written to file.
        converted_scorelist = []
        for entry in scorelist:
            points, player = entry
            converted_scorelist.append([str(points), player])
        scorelist = converted_scorelist

        with open("highscores.json", "w") as hscore_file:
            json.dump(scorelist, hscore_file)
        if len(scorelist) == 1:
            print("Highscore file created.")
        else:
            print("Highscore file updated.")
        return scorelist

    @staticmethod
    def show_highscores(scorelist):
        """Show highscores."""
        time.sleep(4)
        print("\n== Highscores: ==\n")
        if scorelist:
            for rank, entry in enumerate(scorelist, 1):
                print("{}.\t{}\t{}".format(rank, entry[0], entry[1]))
        else:
            print("No entries yet.")
            print("Start a new game and achieve the first highscore!")

    def reset_game(self):
        """Reset game attributes to start a new game."""
        self.current_level = 0
        self.words = self.get_words()
        self.scrambled_words = self.scramble()
        self.level_times = []
        self.hint = True

    def play(self):
        """Show instructions and call game methods."""
        # Check whether words are available.
        if not self.words:
            print("The word file {} couldn't be read!".format(WORD_FILE))
            print("Rename it or change the expected file name (WORD_FILE).")
        else:

            # Show introduction and instructions.
            print("Welcome to SCRAMBLED WORDS.")
            if INSTRUCTIONS:
                print("\nEarn points for each word you can uncramble.")
                print("If you can do it in {} seconds or less,".format(
                    TIME_LIMIT
                ))
                print("you receive bonus points. Press 'H' to see a hint.")
                print("\nDo your best and try to enter the highscore list!")
                time.sleep(6)

            # Run game loop.
            while self.continue_game:
                while self.current_level < self.total_levels:
                    self.next_level()
                    self.challenge()

                # Show results.
                level_points, level_bonus, score = self.get_score()
                self.show_results(level_points, level_bonus, score)

                scorelist = self.get_highscores()
                # Add a new highscore.
                if score:
                    if (len(scorelist) < 10) or (score >= scorelist[-1][0]):
                        scorelist = self.add_highscore(score, scorelist)
                # Show highscores.
                self.show_highscores(scorelist)

                # Ask the user whether to start a new game.
                answer = None
                while answer not in ("y", "yes", "n", "no"):
                    answer = input("\nDo you want to play again? (y/n) ").lower()
                if answer in ("y", "yes"):
                    self.reset_game()
                else:
                    print("Thanks for playing!")
                    self.continue_game = False


######################################################################

# OPTIONS AND FILE NAMES

# Show instructions at the beginning:
INSTRUCTIONS = True

# Maximum number of guesses per word:
MAX_GUESSES = 2

# Time limit for bonus points in seconds:
TIME_LIMIT = 10

# Name of word file:
WORD_FILE = "words_en.txt"

######################################################################


def main():
    """Start the game."""
    sw_game = ScrambledWords()
    sw_game.play()

if __name__ == "__main__":
    main()
