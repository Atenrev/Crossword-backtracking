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


def forward_checking(assigned_word: Word, not_assigned: list, R: np.array, removed: dict):
    for word in not_assigned:
        if word.size == assigned_word.size and assigned_word.word in word.candidates:
            word.candidates.remove(assigned_word.word)
            removed[word.identifier].append(assigned_word.word)
            if not word.candidates:
                return False

        index_1 = R[assigned_word.identifier][word.identifier]
        if index_1 != -1:
            index_2 = R[word.identifier][assigned_word.identifier]

            candidates = []
            for c in word.candidates:
                (removed[word.identifier], candidates)[c[index_2] == assigned_word[index_1]].append(c)
            word.candidates = candidates

            if not word.candidates:
                return False

    return True


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

    index = min(range(0, len(not_assigned)), key=lambda x: len(not_assigned[x].candidates))
    word = not_assigned.pop(index)
    candidates = word.candidates

    removed = {}
    for w in not_assigned:
        removed[w.identifier] = []

    for candidate in candidates:

        word.set_word(candidate)
        if satisfies_restrictions(word, assigned, R):
            success_forward = forward_checking(word, not_assigned, R, removed)
            if success_forward:
                assigned.append(word)
                success, result = backtracking(assigned, not_assigned, R)

                if success:
                    return True, result
                else:
                    assigned.pop()

            for w in not_assigned:
                w.candidates = w.candidates + removed[w.identifier]
                removed[w.identifier] = []

    not_assigned.insert(index, word)
    return False, []
