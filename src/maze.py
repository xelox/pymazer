import time
import random

from window import Window
from cell import Cell
from point import Point


class Maze:
    nesw = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    def __init__(self, win: Window):
        self.cells = []
        self.__win = win
        self.__is_ready = False
        self.__is_generated = False
        self.__is_solved = False
        self.__generation_stack = []
        self.colls = 0
        self.rows = 0
        win.add_update_callback('maze_update', self.__update)
        win.add_update_callback('maze_draw', self.__draw)

    def __clear_maze(self):
        padding = Cell.size
        self.colls = (self.__win.width - padding * 2) // Cell.size
        self.rows = (self.__win.height - padding * 2) // Cell.size
        top = (self.__win.height - self.rows * Cell.size) / 2
        left = (self.__win.width - self.colls * Cell.size) / 2

        for y in range(0, self.rows):
            for x in range(0, self.colls):
                pos = Point(x * Cell.size + left, y * Cell.size + top)
                coord = Point(x, y)
                self.cells.append(Cell(self.__win, pos, coord))

        self.__is_ready = True
        self.__is_generated = False
        self.__is_solved = False
        self.__generation_stack = []
        self.__generation_stack.append(self.cells[0])

    def __generation_step(self):
        print('generation step...')
        if len(self.__generation_stack) == 0:
            print('generation finished...')
            self.__is_generated = True
            return
        current: Cell = self.__generation_stack.pop()
        path_candidates = []
        for d, direction in enumerate(Maze.nesw):
            candidate_coord = current.coord + direction
            if candidate_coord.x < 0:
                continue
            if candidate_coord.y < 0:
                continue
            if candidate_coord.x >= self.colls:
                continue
            if candidate_coord.y >= self.rows:
                continue
            idx = candidate_coord.y * self.colls + candidate_coord.x
            target_cell: Cell = self.cells[idx]
            if target_cell.initial:
                path_candidates.append((target_cell, d))
        if len(path_candidates) > 0:
            dice = random.randint(0, len(path_candidates) - 1)
            print(f"{dice=}")
            choice, d = path_candidates[dice]
            choice.initial = False
            match d:
                case 0: # North
                    current.north = False
                    choice.south = False
                case 1: # Ease
                    current.east = False
                    choice.west = False
                case 2: # South
                    current.south = False
                    choice.north = False
                case 3: # West
                    current.west = False
                    choice.east = False
            self.__generation_stack.append(current)
            self.__generation_stack.append(choice)




    def __solution_step(self):
        pass

    def __update(self):
        if not self.__is_ready:
            self.__clear_maze()
        elif not self.__is_generated:
            self.__generation_step()
        elif not self.__is_solved:
            self.__solution_step()
        else:
            self.__is_ready = False

    def __draw(self):
        self.__win.canvas.delete('all')
        for cell in self.cells:
            cell.draw()
