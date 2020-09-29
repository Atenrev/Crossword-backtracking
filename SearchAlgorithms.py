from Crossword import *
import copy

def satisfies_restrictions(word: Word, LVA: list, R: np.array):
    """
     It returns if the given word satisfies the restrictions of the problem, according to the variables
     previously assigned.
        Args:
            word (object of class Word): The word to check.
            LVA (list): Contains the list of the Word previously assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword)
        Returns:
            (bool): True iif the word satisfies the restrictions
    """

    for variable in LVA:
        if not word.is_compatible(variable, R):
            return False
    return True

"""
La meva idea és que a partir d'ara amaguem tots els mètodes de les classes, amb la funció satisfà restriccions
feta no caldria cridar res en aquelles classes per fer aquesta funció(crec)

No oblidar el que són els paràmetres, no tenen "res" a veure amb la classe crossword ara ja, al main cridariem:

    c = Crossword(a_dict_CB, a_cross_CB)
    bool, list = Backtracking( [], copy.deepcopy(c.words), copy.deepcopy(c.intersections), copy.deepcopy(c.candidates)) (copy deepcopy per si es borra algo)
    if bool:
        c.set_words(list) (si al final definim list com una llista de objectes Word, ja està implementat el set_words)

#########################################################
        JA TINC EL TEST FET --> DESCOMENTAR A TESTCASES.PY PER VEURE SI FUNCIONA
######################################################
    
"""
def backtracking(LVA: list, LVNA: list, R: np.array, D: dict):
    return True, []