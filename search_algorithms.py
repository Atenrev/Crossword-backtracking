import time
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
        index_1 = R[word.identifier][variable.identifier]

        if index_1 != -1:
            index_2 = R[variable.identifier][word.identifier]
            if word[index_1] != variable[index_2]:
                return False

        # if not word.is_compatible(variable, R):
        #     return False
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
        stack_pointer = 0

        if word.size == assigned_word.size and assigned_word.word in word.candidates:
            word.excluded.append(assigned_word.word)
            stack_pointer += 1

            if len(word.excluded) == len(word.candidates):
                word.stack_pointer_list.append(stack_pointer)
                return False

        index_1 = R[assigned_word.identifier][word.identifier]
        if index_1 != -1:
            index_2 = R[word.identifier][assigned_word.identifier]

            for c in word.candidates:
                if c[index_2] != assigned_word[index_1]:
                    word.excluded.append(c)
                    stack_pointer += 1

            if len(word.excluded) == len(word.candidates):
                word.stack_pointer_list.append(stack_pointer)
                return False

        word.stack_pointer_list.append(stack_pointer)

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

    # Afagar el word amb menys candidats
    index = 0
    for i in range(1, len(not_assigned)):
        if len(not_assigned[i].candidates) < len(not_assigned[index].candidates):
            index = i

    word = not_assigned.pop(index)
    candidates = word.candidates
    excluded = word.excluded

    for candidate in candidates:
        if candidate in excluded:
            pass

        word.set_word(candidate)

        if satisfies_restrictions(word, assigned, R):
            part1 = time.time()
            success_forward = forward_checking(word, not_assigned, R)
            part2 = time.time()
            print("FC TIME ==> {}s".format(part2-part1))

            if success_forward:
                assigned.append(word)
                success, result = backtracking(assigned, not_assigned, R)

                if success:
                    return True, result
                else:
                    assigned.pop()

            # part5 = time.time()
            for na in not_assigned:
                if len(na.stack_pointer_list) > 0:
                    pointer = na.stack_pointer_list.pop()
                    del na.excluded[len(na.excluded)-pointer:]
            # part6 = time.time()
            # print("RESET TIME ==> {}s".format(part6-part5))

    not_assigned.insert(index, word)
    return False, []
