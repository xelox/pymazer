class Point: # pylint: disable=too-few-public-methods
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)
