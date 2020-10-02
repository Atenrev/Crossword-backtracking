from crossword import *
from search_algorithms import backtracking


a_cross = "res/crossword_A_v2.txt"
a_dict = "res/diccionari_A.txt"
b_cross = "res/crossword_CB_v2.txt"
b_dict = "res/diccionari_CB_v2.txt"


def main():
    cb = Crossword.from_filenames(b_dict, b_cross)
    success, result = backtracking(
        [],
        copy.deepcopy(cb.words),
        copy.deepcopy(cb.intersections),
        copy.deepcopy(cb.candidates)
    )
    cb.set_words(result)
    cb.print_words()
    print(cb)

    # ca = Crossword.from_filenames(a_dict, a_cross)
    # success, result = backtracking(
    #     [],
    #     copy.deepcopy(ca.words),
    #     copy.deepcopy(ca.intersections),
    #     copy.deepcopy(ca.candidates)
    # )
    # ca.set_words(result)
    # ca.print_words()
    # print(ca)


if __name__ == "__main__":
    main()
