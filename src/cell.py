from point import Point
from window import Window
from line import Line

class Cell: # pylint: disable=too-few-public-methods disable=too-many-instance-attributes
    size = 30
    def __init__(self, win: Window, pos: Point, coord: Point, ):
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.__win = win
        self.coord = coord

        self.center = pos + Point(Cell.size / 2, Cell.size / 2)

        nw = pos
        ne = nw + Point(Cell.size, 0)
        se = ne + Point(0, Cell.size)
        sw = nw + Point(0, Cell.size)
        self.__north_line = Line(nw, ne)
        self.__east_line = Line(ne, se)
        self.__south_line = Line(se, sw)
        self.__west_line = Line(sw, nw)

        self.initial = True

    def draw_move(self, other, undo=False):
        color = 'red'
        if undo:
            color = 'gray'
        self.__win.draw_line(Line(self.center, other.center), color)

    def draw(self):
        if self.north:
            self.__win.draw_line(self.__north_line)
        if self.east:
            self.__win.draw_line(self.__east_line)
        if self.south:
            self.__win.draw_line(self.__south_line)
        if self.west:
            self.__win.draw_line(self.__west_line)
