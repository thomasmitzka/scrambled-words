#!/usr/bin/env python3

"""Scrambled Words is a text-based word guessing game.

The player has to guess the correct order of letters in a word
throughout several levels. Scrambled words are created from a text
file. Each level presents a more difficult word scramble. After a
limited number of guesses, the level ends.

Once in every game, the player can get a hint to help in guessing the
word. In the end, the player receives points for solved words, and
bonus points for completing levels within a time limit. When the first
highscore is achieved, the game creates a text file to store highscore
entries.
"""

import random
import time


class ScrambledWords():
    """The main class of the game.

    It provides methods to read and scramble words, ask for user input,
    create a hint, read and show highscores, add new highscores and
    write them to file.
    """

    def __init__(self):
        """Initialize class variables.

        Call methods get_words() and scramble() to create a list
        of scrambled words.
        """
        self.words = self.get_words()
        self.scrambled_words = self.scramble()
        self.level = 0
        self.hint = True
        self.times = []
        self.score = 0

    def __repr__(self):
        """Return information on class."""
        return "A text-based word guessing game."

    @staticmethod
    def get_words():
        """Read words from file and return a list of random words."""
        try:
            with open(WORD_FILE, "r") as file:
                lines = [line.strip().split(",") for line in file]
        except FileNotFoundError:
            print("Word file {} could not be read!".format(
                WORD_FILE
            ))
        words = [random.choice(element).upper() for element in lines]
        return words

    def scramble(self):
        """Scramble words in list, and return list."""
        scrambled_words = []
        for word in self.words:
            scrambled_word = word
            while scrambled_word == word:
                letters = list(scrambled_word)
                random.shuffle(letters)
                scrambled_word = "".join(letters)
            scrambled_words.append(scrambled_word)
        return scrambled_words

    def next_level(self):
        """Raise level counter and start countdown to next level."""
        self.level += 1
        print("Get ready for level {} ...".format(self.level))
        time.sleep(4)

    def challenge(self):
        """Show scrambled word, take user input, and measure time.

        End level if the word has been solved or if guess limit has
        been reached. The hint option is not available if the word has
        less than five letters, because create_hint() corrects the
        first three letters.
        """
        scrambled_word = self.scrambled_words[self.level - 1]
        word = self.words[self.level - 1]
        guesses = MAX_GUESSES

        # Save start time:
        start = time.time()

        print("\n== Level {} of {} ({} points) ==".format(
            self.level, LEVELS, self.level * 10
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
            # Save finish and level time:
            finish = time.time()
            self.times.append(round((finish - start), 1))

            print(random.choice(("Well done!", "Great!", "Awesome!")), end=" ")
            print("You finished this level in {} seconds.".format(
                self.times[-1]
            ))
        else:
            self.times.append(0)
            print("You didn't guess this one.")

    @staticmethod
    def create_hint(word):
        """Create and return new string as a hint.

        Take the correct word as argument. Keep the first three
        letters, and shuffle the rest.
        """
        letters = list(word)
        part1 = letters[:3]
        part2 = letters[3:]
        while part2 == letters[3:]:
            random.shuffle(part2)

        print("You requested a hint. Here it comes:")
        return "".join(part1) + "".join(part2)

    def show_score(self):
        """Calculate and show level scores and total score.

        A level time of 0 means that the word was not solved.
        Add bonus points if the level time doesn't exceed the
        time limit.
        """
        points = []
        bonus = []

        for i in range(LEVELS):
            if self.times[i]:
                points.append((i + 1) * 10)

                if self.times[i] <= TIME_LIMIT:
                    bonus.append((i + 1) * 10)
                else:
                    bonus.append(0)

            else:
                points.append(0)
                bonus.append(0)

        time.sleep(4)
        print("\n== Results: ==")
        print("\nLvl\tPts\tBonus\tTime (sec)")
        for i in range(LEVELS):
            print("{}\t{}\t{}\t".format(i + 1, points[i], bonus[i]), end="")
            if self.times[i] > 0:
                print(self.times[i])
            else:
                print("-")

        for level_points in points:
            self.score += level_points
        for level_bonus in bonus:
            self.score += level_bonus
        print("\nYour total score: {}".format(self.score))

    def show_highscores(self):
        """Read highscores from file and show them.

        If a new highscore has been achieved, save the player's name
        and score by calling method add_highscore(). Highscores are
        stored in a text file. There can only be 10 highscore entries
        at a time. A new highscore must at least be as high as the
        lowest (= last) entry in the list.
        """
        try:
            with open(HSCORE_FILE, "r") as file:
                scorelist = [line.strip().split(";") for line in file]
                # Convert the score numbers to integer,
                # so they can be compared and sorted.
                for entry in scorelist:
                    entry[0] = int(entry[0])
        except FileNotFoundError:
            scorelist = []

        if self.score:
            if ((len(scorelist) < 10) or
                    (len(scorelist) >= 10 and self.score >= scorelist[-1][0])):
                scorelist = self.add_highscore(scorelist)

        time.sleep(4)
        print("\n== Highscores: ==\n")
        if scorelist:
            for entry in scorelist:
                print("{}\t{}".format(entry[0], entry[1]))
        else:
            print("No entries yet.")
            print("Start a new game and achieve the first highscore!")

    def add_highscore(self, scorelist):
        """Add a new highscore, write list to file, and return list.

        If the list already contains ten or more highscore entries,
        remove the last entries before adding the new one. Sort the
        list before writing and returning it.
        """
        print("\n** NEW HIGHSCORE **")
        print("Please enter your name:")
        username = ""
        while username == "":
            username = input("> ")
        print("\nCongratulations, {}!".format(username))

        while len(scorelist) >= 10:
            scorelist.pop()

        scorelist.append([self.score, username])
        scorelist = sorted(scorelist, reverse=True)

        # Convert score values from integer to string,
        # so they can be joined and written to file.
        for item in scorelist:
            item[0] = str(item[0])

        lines = [";".join(item) for item in scorelist]

        with open(HSCORE_FILE, "w") as file:
            for line in lines:
                file.write(line + "\n")
        if len(lines) == 1:
            print("Highscore file {} created.".format(HSCORE_FILE))
        else:
            print("Highscore file updated.")
        return scorelist

    def play(self):
        """Show instructions and call game methods.

        Check whether there are enough lines in the word file for the
        chosen number of levels."""
        if LEVELS > len(self.words):
            print("There are only {} sets of words for {} levels!".format(
                len(self.words), LEVELS
            ))
            print("Please set a lower level number or add more lines")
            print("in your word file: {}".format(WORD_FILE))
        else:

            print("Welcome to SCRAMBLED WORDS.")
            if INSTRUCTIONS:
                print("\nEarn points for each word you can uncramble.")
                print("If you can do it in {} seconds or less,".format(
                    TIME_LIMIT
                ))
                print("you receive bonus points. Press 'H' to see a hint.")
                print("\nDo your best and try do enter the highscore list!")
                time.sleep(6)

            while self.level < LEVELS:
                self.next_level()
                self.challenge()
            self.show_score()
            self.show_highscores()


######################################################################

# OPTIONS AND FILE NAMES

# Show instructions at the beginning:
INSTRUCTIONS = True

# Number of levels (must not exceed number of lines in word file):
LEVELS = 6

# Maximum number of guesses per word:
MAX_GUESSES = 2

# Time limit for bonus points in seconds:
TIME_LIMIT = 10

# Name of highscore file (will be created if required):
HSCORE_FILE = "highscores.txt"

# Name of word file
WORD_FILE = "words_en.txt"

######################################################################


def main():
    """Start the game."""
    sw_game = ScrambledWords()
    sw_game.play()

if __name__ == "__main__":
    main()
