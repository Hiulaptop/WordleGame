import random
import time
from collections import Counter

class Words:
    def __init__(self):
        random.seed(time.time())
        self._words = self._load_words()
        self._word = None
        # pick an initial random word if the list isn't empty
        if self._words:
            self.get_random_word()
        print(self._word)

    def _load_words(self):
        with open('assets/words-list.txt', "r") as f:
            return [line.strip().upper() for line in f if len(line.strip()) == 5]

    def _is_valid_word(self, word):
        return word.upper() in self._words

    def _print(self):
        print(self._word)

    def get_random_word(self):
        if not self._words:
            raise ValueError("Word list is empty")
        idx = random.randrange(len(self._words))
        self._word = self._words[idx]
        return self._word

    def check_word(self, word):
        # Normalize and validate
        guess = word.strip().upper()
        if len(guess) != 5 or not self._is_valid_word(guess):
            return False

        # Prepare result and counts
        result = [""] * 5
        counts = Counter(self._word)

        # First pass: mark greens and decrement counts
        for idx, ch in enumerate(guess):
            if ch == self._word[idx]:
                result[idx] = "GREEN"
                counts[ch] -= 1

        # Second pass: mark yellows or blacks
        for idx, ch in enumerate(guess):
            if result[idx] == "":
                if counts.get(ch, 0) > 0:
                    result[idx] = "YELLOW"
                    counts[ch] -= 1
                else:
                    result[idx] = "BLACK"

        print(result)
        return result