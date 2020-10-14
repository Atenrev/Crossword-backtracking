from crossword import *
from search_algorithms import backtracking
import time


a_cross = "res/crossword_A_v2.txt"
a_dict = "res/diccionari_A.txt"
b_cross = "res/crossword_CB_v2.txt"
b_dict = "res/diccionari_CB_v2.txt"


def main():
    a_cross_medium = "test/crossword_medium.txt"
    a_dict_medium = "test/diccionari_medium.txt"
    cw_medium = Crossword.from_filenames(a_dict_medium, a_cross_medium)
    solucio_medium, words_medium = backtracking(
        [], copy.deepcopy(cw_medium.words), cw_medium.intersections)

    cb = Crossword.from_filenames(b_dict, b_cross)
    success, result = backtracking(
        [],
        copy.deepcopy(cb.words),
        copy.deepcopy(cb.intersections),
    )
    cb.set_words(result)
    # cb.print_words()
    print(cb)

    ca = Crossword.from_filenames(a_dict, a_cross)
    start = time.time()
    success, result = backtracking(
        [], copy.deepcopy(ca.words), ca.intersections)
    end = time.time()
    print(end-start)
    ca.set_words(result)
    ca.print_words()
    print(ca)


if __name__ == "__main__":
    main()
