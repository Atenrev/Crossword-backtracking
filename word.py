import numpy as np


class Word:
    """
    A class for keeping all the data regarding one variable of the problem ( a word space on the crossword)

    self.size: An int containing the number of letters in the word

    self.identifier: An identifier (int) to differentiate the variables (starting at 0)

    self.word: An string empty at the start, to be filled with the corresponding word found
    """

    def __init__(self, size: int, identifier: int, candidates: list):
        self.identifier = identifier
        self.size = size
        self.word = ""
        self.candidates = set(candidates)
        self.removed = []

    def set_word(self, word: str):
        self.word = word

    def resize(self, size: int):
        self.size = size

    def get_identifier(self):
        return self.identifier

    def get_size(self):
        return self.size

    def is_compatible_word(self, word, intersections: np.array):
        """
         Given a word and a matrix of intersections, it returns if the word is compatible
         with self in the crossword (on the corresponding positions)
            Args:
                word (object of class Word): The second word.
                intersections (numpy matrix): A matrix containing the intersections of the crossword.
            Returns:
                (bool): True iif the words are compatible.
        """
        index_1 = intersections[self.identifier][word.identifier]

        if index_1 != -1:
            index_2 = intersections[word.identifier][self.identifier]
            return self[index_1] == word[index_2]

        return True

    def is_compatible(self, word, intersections: np.array):
        """
         Given a word and a matrix of intersections, it returns if the word is compatible
         with self in the crossword (on the corresponding positions)
            Args:
                word (object of class Word): The second word.
                intersections (numpy matrix): A matrix containing the intersections of the crossword.
            Returns:
                (bool): True iif the words are compatible.
        """
        index_1 = intersections[self.identifier][word.identifier]

        if index_1 != -1:
            index_2 = intersections[word.identifier][self.identifier]
            return self[index_1] == word[index_2]

        return True

    def __eq__(self, other):
        return self.word == other

    def __str__(self):
        return self.word

    def __getitem__(self, letter: int):  # operator []
        if letter < self.size:
            return self.word[letter]
