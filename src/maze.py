import time

from window import Window
from cell import Cell
from point import Point

class Maze:
    def __init__(self, win: Window):
        self.cells = []
        self.__win = win
        padding = Cell.size
        width = (win.width - padding * 2) // Cell.size
        height = (win.height - padding * 2) // Cell.size
        top = (win.height - height * Cell.size) / 2
        left = (win.width - width * Cell.size) / 2

        for y in range(0, height):
            for x in range(0, width):
                p = Point(x * Cell.size + left, y * Cell.size + top)
                self.cells.append(Cell(win, p))

        win.add_update_callback('maze_draw', self.__draw)

    def __draw(self):
        self.__win.canvas.delete('all')
        for cell in self.cells:
            cell.draw()
