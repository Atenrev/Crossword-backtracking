from crossword import *
import copy


def satisfies_restrictions(word: Word, assigned: list, R: np.array):
    """
     It returns if the given word satisfies the restrictions of the problem, according to the variables
     previously assigned.
        Args:
            word (object of class Word): The word to check.
            assigned (list): Contains the list of the Word previously assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword).
        Returns:
            (bool): True if the word satisfies the restrictions.
    """

    for variable in assigned:
        if not word.is_compatible(variable, R):
            return False
    return True



def backtracking_raw(assigned: list, not_assigned: list, R: np.array, C: dict):
    """
     Recursive method that will try to fill in all the whitespaces of the crossword.
        Args:
            assigned (list): Contains the list of the Word previously assigned.
            not_assigned (list): Contains the list of the Word to be assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword).
            R (dict): Dictionary containing all the candidates for each size.
        Returns:
            (bool): True if a solution is found.
            (list): List containing the solution (in case that it exists).
    """

    if not_assigned == []:
        return True, assigned

    word = not_assigned[0]

    for candidate in C[word.size]:
        word.set_word(candidate)

        if satisfies_restrictions(word, assigned, R):
            idx = C[word.size].index(candidate)
            C[word.size].remove(candidate)
            assigned.append(not_assigned.pop(0))
            success, result = backtracking_raw(
                assigned, not_assigned, R, C)

            if success:
                return True, result
            else:
                not_assigned.insert(0, assigned.pop())
                C[word.size].insert(idx, candidate)

    return False, []


def forward_checking(assigned_word: Word, not_assigned: list, R: np.array):
    for word in not_assigned:
        if word.size == assigned_word.size and assigned_word.word in word.candidates: #abans estava al backtracking, m'ho porto aquí per no recòrrer dos cops la mateixa llista, afegeixo lo del size per no fer cerca en la llista si no cal
            word.candidates.remove(assigned_word.word)
            if not word.candidates: #no serveix amb lo d'abaix, potser tenen el mateix tamany i no interseccionen
                return False, []

        index_1 = R[assigned_word.identifier][word.identifier]
        if index_1 != -1:
            index_2 = R[word.identifier][assigned_word.identifier]
            word.candidates = [c for c in word.candidates if c[index_2] == assigned_word[index_1]] #això s'ha de fer a pal sec, si cridem al is_compatible en bucle és mortal

            if not word.candidates:  #si en algun moment una paraula no té candidats, podem
                return False, []

    return True, not_assigned


def backtracking(assigned: list, not_assigned: list, R: np.array):
    """
     Recursive method that will try to fill in all the whitespaces of the crossword.
        Args:
            assigned (list): Contains the list of the Word previously assigned.
            not_assigned (list): Contains the list of the Word to be assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword).
        Returns:
            (bool): True if a solution is found.
            (list): List containing the solution (in case that it exists).
    """

    if not not_assigned:
        return True, assigned

    word = not_assigned.pop(0)
    candidates = word.candidates

    for candidate in candidates:
        word.set_word(candidate)

        success_forward, result_forward = forward_checking(word, copy.deepcopy(not_assigned), R)
        if satisfies_restrictions(word, assigned, R) and success_forward:
            assigned.append(word)
            new_not_assigned = result_forward

            success, result = backtracking(copy.deepcopy(assigned), copy.deepcopy(new_not_assigned), R)

            if success:
                return True, result
            else:
                assigned = assigned[:-1]

    return False, []
