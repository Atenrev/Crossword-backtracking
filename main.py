from Crossword import *
a_cross = "res/crossword_CB_v2.txt"
a_dict = "res/diccionari_CB_v2.txt"


def main():
    c = Crossword(a_dict, a_cross)

    print(np.array_equal(b, c.intersections))





if __name__ == "__main__":
    main()
