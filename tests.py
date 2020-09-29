import unittest
from search_algorithms import *
from crossword import *
import os
import operator


class TestCases(unittest.TestCase):

    def setUp(self):
        a_cross_CB = "res/crossword_CB_v2.txt"
        a_dict_CB = "res/diccionari_CB_v2.txt"
        self.cw_CB = Crossword(a_dict_CB, a_cross_CB)

        a_cross_A = "res/crossword_A_v2.txt"
        a_dict_A = "res/diccionari_A.txt"
        self.cw_A = Crossword(a_dict_A, a_cross_A)

        a_cross_empty = "test/crossword_empty.txt"
        a_dict_empty = "test/diccionari_empty.txt"
        self.cw_empty = Crossword(a_dict_empty, a_cross_empty)

        a_cross_short = "test/crossword_short.txt"
        a_dict_short = "test/diccionari_short.txt"
        self.cw_short = Crossword(a_dict_short, a_cross_short)

        a_cross_medium = "test/crossword_medium.txt"
        a_dict_medium = "test/diccionari_medium.txt"
        self.cw_medium = Crossword(a_dict_medium, a_cross_medium)

    def test_exists_intersection(self):
        coordinates_1 = WordCoordinates(0, 0, Direction.HORIZONTAL, 5)
        coordinates_2 = WordCoordinates(20, 26, Direction.HORIZONTAL, 48)
        coordinates_3 = WordCoordinates(0, 0, Direction.VERTICAL, 6)
        coordinates_4 = WordCoordinates(0, 30, Direction.VERTICAL, 22)

        self.assertEqual(coordinates_1.exists_intersection(
            coordinates_2)[0], False)
        self.assertEqual(coordinates_3.exists_intersection(
            coordinates_4)[0], False)
        self.assertEqual(coordinates_1.exists_intersection(
            coordinates_4)[0], False)
        self.assertEqual(coordinates_2.exists_intersection(
            coordinates_3)[0], False)
        self.assertEqual(coordinates_1.exists_intersection(
            coordinates_3), (True, 0, 0))
        self.assertEqual(coordinates_2.exists_intersection(
            coordinates_4), (True, 4, 20))
        self.assertEqual(coordinates_4.exists_intersection(
            coordinates_2), (True, 20, 4))

    def test_find_intersections(self):
        m_CB = np.array([[-1, 0, 3, 5, -1, -1, -1, -1, -1, -1],
                         [0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [0, -1, -1, -1, 2, 4, -1, -1, -1, 5],
                         [0, -1, -1, -1, 2, 4, -1, -1, -1, -1],
                         [-1, -1, 1, 3, -1, -1, -1, -1, -1, -1],
                         [-1, -1, 2, 4, -1, -1, 0, 1, 3, -1],
                         [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
                         [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
                         [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
                         [-1, -1, 3, -1, -1, -1, 1, 2, 4, -1]]).astype(np.intc)
        m_empty = -np.ones((0, 0)).astype(np.intc)
        m_short = np.array([[-1, 3, -1],
                            [0, -1, 3],
                            [-1, 1, -1]]).astype(np.intc)
        m_medium = np.array([[-1, 1, 3, 5, -1],
                             [0, -1, -1, -1, 5],
                             [0, -1, -1, -1, 5],
                             [0, -1, -1, -1, 5],
                             [-1, 1, 3, 5, -1]]).astype(np.intc)

        self.assertTrue(np.array_equal(m_CB, self.cw_CB.intersections))
        self.assertTrue(np.array_equal(m_empty, self.cw_empty.intersections))
        self.assertTrue(np.array_equal(m_short, self.cw_short.intersections))
        self.assertTrue(np.array_equal(m_medium, self.cw_medium.intersections))

    def test_analyze_crossword_board(self):
        nWords_A = 50
        coordinates_CB = {0: WordCoordinates(0, 0, Direction.HORIZONTAL, 6),
                          1: WordCoordinates(0, 0, Direction.VERTICAL, 4),
                          2: WordCoordinates(0, 3, Direction.VERTICAL, 6),
                          3: WordCoordinates(0, 5, Direction.VERTICAL, 5),
                          4: WordCoordinates(2, 2, Direction.HORIZONTAL, 4),
                          5: WordCoordinates(4, 1, Direction.HORIZONTAL, 5),
                          6: WordCoordinates(4, 1, Direction.VERTICAL, 2),
                          7: WordCoordinates(4, 2, Direction.VERTICAL, 2),
                          8: WordCoordinates(4, 4, Direction.VERTICAL, 2),
                          9: WordCoordinates(5, 0, Direction.HORIZONTAL, 5)
                          }
        coordinates_empty = {}
        coordinates_short = {0: WordCoordinates(0, 0, Direction.HORIZONTAL, 4),
                             1: WordCoordinates(0, 3, Direction.VERTICAL, 4),
                             2: WordCoordinates(3, 2, Direction.HORIZONTAL, 2)}
        coordinates_medium = {0: WordCoordinates(0, 0, Direction.HORIZONTAL, 6),
                              1: WordCoordinates(0, 1, Direction.VERTICAL, 6),
                              2: WordCoordinates(0, 3, Direction.VERTICAL, 6),
                              3: WordCoordinates(0, 5, Direction.VERTICAL, 6),
                              4: WordCoordinates(5, 0, Direction.HORIZONTAL, 6)}

        self.assertDictEqual(coordinates_empty, self.cw_empty.coordinates)
        self.assertEqual(nWords_A, len(self.cw_A.coordinates))
        self.assertDictEqual(coordinates_CB, self.cw_CB.coordinates)
        self.assertDictEqual(coordinates_short, self.cw_short.coordinates)
        self.assertDictEqual(coordinates_medium, self.cw_medium.coordinates)

    def test_read_candidates(self):
        nCandidates_CB = 102
        candidates_empty = {}
        candidates_short = {2: ["TU"],
                            3: ["BON", "DIA"],
                            4: ["HOLA", "ADEU", "FINS"],
                            7: ["DESPRES"]}
        candidates_medium = {4: ["JOAN", "PERE"],
                             6: ["PATATA", "PERICO", "ALUMNE", "AUXILI", "APOLLO", "PIRATA", "SASTRE"]}

        self.assertEqual(nCandidates_CB, sum(len(value)
                                             for value in self.cw_CB.candidates.values()))
        self.assertDictEqual(candidates_empty, self.cw_empty.candidates)
        self.assertDictEqual(candidates_medium, self.cw_medium.candidates)
        self.assertDictEqual(candidates_short, self.cw_short.candidates)

    def test_satisfies_restrictions(self):
        lva = []
        for i in range(3):
            lva.append(Word(6, i))
        lva[0].set_word("PATATA")
        lva[1].set_word("ALUMNE")
        lva[2].set_word("AUXILI")

        word_1 = Word(6, 3)
        word_1.set_word("SASTRE")
        word_2 = Word(6, 3)
        word_2.set_word("APOLLO")
        word_3 = Word(6, 4)
        word_3.set_word("PIRATA")
        word_4 = Word(6, 4)
        word_4.set_word("PERICO")

        self.assertFalse(satisfies_restrictions(
            word_1, lva, self.cw_medium.intersections))
        self.assertTrue(satisfies_restrictions(
            word_2, lva, self.cw_medium.intersections))
        self.assertFalse(satisfies_restrictions(
            word_3, lva, self.cw_medium.intersections))
        self.assertTrue(satisfies_restrictions(
            word_4, lva, self.cw_medium.intersections))

    def test_backtracking(self):

        expected_words_medium = []
        for i in range(5):
            expected_words_medium.append(Word(6, i))
        expected_words_medium[0].set_word("PATATA")
        expected_words_medium[1].set_word("ALUMNE")
        expected_words_medium[2].set_word("AUXILI")
        expected_words_medium[3].set_word("APOLLO")
        expected_words_medium[4].set_word("PERICO")

        expected_words_short = [Word(4, 0), Word(4, 1), Word(2, 2)]
        expected_words_short[0].set_word("HOLA")
        expected_words_short[1].set_word("ADEU")
        expected_words_short[2].set_word("TU")

        solucio_short, words_short = backtracking([], copy.deepcopy(self.cw_short.words),
                                                  copy.deepcopy(
                                                      self.cw_short.intersections),
                                                  copy.deepcopy(self.cw_short.candidates))

        solucio_medium, words_medium = backtracking([], copy.deepcopy(self.cw_medium.words),
                                                    copy.deepcopy(
                                                        self.cw_medium.intersections),
                                                    copy.deepcopy(self.cw_medium.candidates))

        # self.assertTrue(solucio_short)
        # self.assertTrue(solucio_medium)
        #self.assertListEqual(words_medium, expected_words_medium)
        #self.assertListEqual(words_short, expected_words_short)
