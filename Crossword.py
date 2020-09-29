__authors__ = 'Biel Castaño Segade\nSergi Masip Cabeza\nJordi Xhafa Daci'
# _________________________________________________________________________________________
# Coneixement, Raonament i Incertesa
# Grau en Enginyeria Informatica
# Curs 2020- 2021
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________


import numpy as np
from word import *
from word_coordinates import *
WHITE = '0'
BLACK = '#'


def read_crossword_board(filename: str):
    """
     It reads a text file with WHITE and BLACK characters and returns the equivalent matrix.
        Args:
            filename (str): Name of the file containing the data (in matrix format).
        Returns:
            board (list of list): Matrix containing the BLACK and WHITE characters of the board.
    """

    board = []
    with open(filename, 'r') as f:
        for line in f:
            row = line.split('\n')[0]
            board.append(row.split('\t'))
    return board


def search_horizontal_word(crossword_board: list, row: int, col: int):
    """
     Given a board, a row and a column, it returns if there are any horizontal word starting at the corresponding square
     of the board. If affirmative, it also returns the size of the word.
        Args:
            crossword_board (list of list): Matrix containing the BLACK and WHITE characters of the board.
            row (int): Number of the considered row.
            col (int): Number of the considered column.
        Returns:
            (bool): Indicates if there are any horizontal word starting at the considered square.
            size (int): The size of the word (if it exists).
    """

    n = len(crossword_board)
    if (col == 0 or crossword_board[row][col-1] == BLACK) and (col < n-1) \
            and (crossword_board[row][col+1] == WHITE):  # new horizontal word
        size = 0
        while col < n and crossword_board[row][col] == WHITE:
            size += 1
            col += 1
        return True, size
    else:
        return False, -1


def search_vertical_word(crossword_board: list, row: int, col: int):
    """
     Given a board, a row and a column, it returns if there are any vertical word starting at the corresponding square
     of the board. If affirmative, it also returns the size of the word.
        Args:
            crossword_board (list of list): Matrix containing the BLACK and WHITE characters of the board.
            row (int): Number of the considered row.
            col (int): Number of the considered column.
        Returns:
            (bool): Indicates if there are any vertical word starting at the considered square.
            size (int): The size of the word (if it exists).
    """

    n = len(crossword_board)
    if (row == 0 or crossword_board[row-1][col] == BLACK) and (row < n - 1) \
            and (crossword_board[row+1][col] == WHITE):  # new vertical word
        size = 0
        while row < n and crossword_board[row][col] == WHITE:
            size += 1
            row += 1
        return True, size
    else:
        return False, -1


class Crossword:
    """
    A class for keeping all the data regarding a crossword


    self.candidates: is a dictionary of list holding all the word candidates of each size, with the next format
            {
                size_1 : [word_1_with_size_1, word_2_with_size_1, ...],
                size_2 : [word_1_with_size_2, word_2_with_size_2, ...],
                ....
            }

    self.words: is a list of Word corresponding to the variables of the crossword

    self.intersections: a matrix containing the intersections of the crossword's words, where the coordinate
            (i,j) indicates in witch letter (starting at 0) of the word  with identifier i there is an intersection
            with the word with identifier j (if there isn't any connection, the value is -1)

    self.coordinates: is a dictionary containing the coordinates of each word on the crossword, where the keys are
            the identifiers of the words and the values are WordCoordinates objects
            {
                identifier_1 : WordCoordinates_1,
                identifier_2 : WordCoordinates_2,
                ....
            }

    """

    def __init__(self,  filename_dictionary: str, filename_crossword: str):
        self.candidates = {}
        self.words = []
        self.intersections = []
        self.coordinates = {}

        self.read_candidates(filename_dictionary)

        crossword_board = read_crossword_board(filename_crossword)
        self.analyze_crossword_board(crossword_board)
        self.find_intersections()

    def read_candidates(self, filename: str):
        """
         It reads the information of the candidate words from a file.
            Args:
                filename (str): Name of the file containing the words (separated by '\n')
        """

        with open(filename, 'r') as f:
            for line in f:
                candidate = line.split('\n')[0]
                if len(candidate) in self.candidates:
                    self.candidates[len(candidate)].append(candidate)
                else:
                    self.candidates[len(candidate)] = [candidate]

    def analyze_crossword_board(self, crossword_board: list):
        """
         Given a board, it searches all the spaces for words and stores the corresponding information on
         self.words and self.coordinates.
            Args:
                crossword_board (list of list): Matrix containing the BLACK and WHITE characters of the board.
        """

        identifier = 0
        n = len(crossword_board)

        for i in range(n):
            for j in range(n):
                if crossword_board[i][j] == WHITE:

                    horizontal_word, horizontal_size = search_horizontal_word(
                        crossword_board, i, j)
                    vertical_word, vertical_size = search_vertical_word(
                        crossword_board, i, j)

                    if horizontal_word:
                        self.words.append(Word(horizontal_size, identifier))
                        self.coordinates[identifier] = WordCoordinates(
                            i, j, Direction.HORIZONTAL, horizontal_size)
                        identifier += 1

                    if vertical_word:
                        self.words.append(Word(vertical_size, identifier))
                        self.coordinates[identifier] = WordCoordinates(
                            i, j, Direction.VERTICAL, vertical_size)
                        identifier += 1

    def find_intersections(self):
        """
         It searches the intersections on the board from the information stored on self.coordinates.
        """

        n = len(self.words)
        self.intersections = -np.ones((n, n)).astype(np.intc)

        for i in range(n):
            for j in range(i+1, n):
                intersection, position_1, position_2 = self.coordinates[i].exists_intersection(
                    self.coordinates[j])
                if intersection:
                    self.intersections[i][j] = position_1
                    self.intersections[j][i] = position_2

    def set_word(self, identifier: int, word: str):
        for w in self.words:
            if w.identifier == identifier:
                w.set_word(word)
                return True
        return False

    def set_words(self, words: list):
        for word in words:
            self.set_word(word.identifier, word.word)

    def print_words(self):
        words_aux = self.words
        words_aux.sort(key=Word.get_identifier)
        for i in range(len(words_aux)):
            word = words_aux[i]
            print("Paraula ", i, ": ", word.word)
            self.coordinates[word.identifier].print_coordinates()
            print("\n")
