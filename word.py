class Word:
    x = 0
    y = 0
    size = 0
    horizontal = True
    word = ""

    def __init__(self, x: int, y: int, size: int, horizontal: bool):
        self.x, self.y = x, y
        self.size = size
        self.horizontal = horizontal
