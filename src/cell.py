from point import Point
from window import Window
from line import Line

class Cell: # pylint: disable=too-few-public-methods disable=too-many-instance-attributes
    size = 30
    def __init__(self, win: Window, coord: Point, ):
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.__win = win

        nw = coord
        ne = nw + Point(Cell.size, 0)
        se = ne + Point(0, Cell.size)
        sw = nw + Point(0, Cell.size)
        self.north_line = Line(nw, ne)
        self.east_line = Line(ne, se)
        self.south_line = Line(se, sw)
        self.west_line = Line(sw, nw)

    def draw(self):
        if self.north:
            self.__win.draw_line(self.north_line)
        if self.east:
            self.__win.draw_line(self.east_line)
        if self.south:
            self.__win.draw_line(self.south_line)
        if self.west:
            self.__win.draw_line(self.west_line)
