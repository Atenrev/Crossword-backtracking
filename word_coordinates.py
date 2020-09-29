from enum import Enum


class Direction(Enum):
    HORIZONTAL = True
    VERTICAL = False


class WordCoordinates:
    """
    A class for keeping all the data regarding the position of a word in the crossword

    self.i: An int containing the first coordinate of the first letter of the word (starting at 0)

    self.j: An int containing the second coordinate of the first letter of the word (starting at 0)

    self.direction: A bool that indicates the direction of the word
            (horizontal from left to right or vertical from top to bottom)

    self.size: An int containing the number of letters in the word
    """

    def __init__(self, x: int, y: int, direction: Direction, size: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size

    def __eq__(self, word_coordinates):
        return self.x == word_coordinates.x and self.y == word_coordinates.y \
               and self.direction == word_coordinates.direction and self.size == word_coordinates.size

    def __hash__(self):
        return hash((self.x, self.y, self.direction, self.size))

    def exists_intersection_horizontal(self, word_coordinates_vertical):
        """
         If self.direction is horizontal, given other coordinates of a vertical word, it returns if there is
         an intersection between the words, if affirmative, it also returns in which position relative to each word.
            Args:
                word_coordinates_vertical (object of class WordCoordinates): The second coordinates.
            Returns:
                (bool): True iif there is an intersection between the two words.
                position_horizontal (int): Position of the intersection on the horizontal word.
                position_vertical (int): Position of the intersection on the vertical word.
        """

        position_horizontal = word_coordinates_vertical.y - self.y
        position_vertical = self.x - word_coordinates_vertical.x
        if 0 <= position_horizontal < self.size and 0 <= position_vertical < word_coordinates_vertical.size:
            return True, position_horizontal, position_vertical
        return False, -1, -1

    def exists_intersection_vertical(self, word_coordinates_horizontal):
        """
         If self.direction is vertical, given other coordinates of a horizontal word, it returns if there is
         an intersection between the words, if affirmative, it also returns in which position relative to each word.
            Args:
                word_coordinates_vertical (object of class WordCoordinates): The second coordinates.
            Returns:
                (bool): True iif there is an intersection between the two words.
                position_horizontal (int): Position of the intersection on the horizontal word.
                position_vertical (int): Position of the intersection on the vertical word.
        """

        exists, position_horizontal, position_vertical = \
            word_coordinates_horizontal.exists_intersection_horizontal(self)
        return True, position_vertical, position_horizontal

    def exists_intersection(self, word_coordinates):
        """
         Given the coordinates of a word, it returns if it has an intersection with the word given by self,
          if affirmative, it also returns in which position relative to each word.
            Args:
                word_coordinates (object of class WordCoordinates): The second coordinates.
            Returns:
                (bool): True iif there is an intersection between the two words.
                position_horizontal (int): Position of the intersection on the word represented by self.
                position_vertical (int): Position of the intersection on the word represented by word_coordinates.
        """
        if self.direction != word_coordinates.direction: #if not, we assume there is no intersection
            if self.direction == Direction.HORIZONTAL:
                return self.exists_intersection_horizontal(word_coordinates)
            return self.exists_intersection_vertical(word_coordinates)
        return False, -1, -1

    def print_coordinates(self):
        direction = "Vertical"
        if self.direction == Direction.HORIZONTAL:
            direction = "Horitzontal"
        print("Coordenades: (", self.x, ",", self.y, "), Direcció: ", direction, ", Tamany: ", self.size)

