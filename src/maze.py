import time
import random

from window import Window
from cell import Cell
from point import Point
from line import Line


class Node: # pylint: disable=too-few-public-methods
    def __init__(self, cell: Cell):
        self.cell = cell
        self.parent = None

class Maze:
    nesw = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    def __init__(self, win: Window):
        self.cells = []
        self.__win = win
        self.__is_ready = False
        self.__is_generated = False
        self.__is_solved = False
        self.__generation_stack = []
        self.__open_set = []
        self.colls = 0
        self.rows = 0
        self.__head = None
        self.__win.set_update_timeout(0.05)
        win.add_update_callback('maze_update', self.__update)
        win.add_update_callback('maze_draw', self.__draw)

    def __clear_maze(self):
        padding = Cell.size
        self.cells = []
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
        self.__open_set = []
        self.__generation_stack.append(self.cells[0])
        self.__open_set.append(Node(self.cells[0]))
        self.__head = None
        print('maze reset')

    def __generation_step(self):
        if len(self.__generation_stack) == 0:
            print('generation finished')
            self.__is_generated = True
            return
        current: Cell = self.__generation_stack.pop()
        path_candidates = []
        for d, direction in enumerate(Maze.nesw):
            candidate_coord = current.coord + direction
            if (
                candidate_coord.x < 0 or
                candidate_coord.y < 0 or
                candidate_coord.x >= self.colls or
                candidate_coord.y >= self.rows
            ):
                continue
            idx = candidate_coord.y * self.colls + candidate_coord.x
            target_cell: Cell = self.cells[idx]
            if target_cell.initial:
                path_candidates.append((target_cell, d))
        if len(path_candidates) > 0:
            dice = random.randint(0, len(path_candidates) - 1)
            choice, d = path_candidates[dice]
            choice.initial = False
            match d:
                case 0: # North
                    current.north = False
                    choice.south = False
                case 1: # East
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
        if len(self.__open_set) == 0:
            self.__is_solved = True
            print('unsolvable')
            return
        current_node: Node = self.__open_set.pop()
        self.__head = current_node
        current: Cell = current_node.cell
        current.closed = True
        if current.coord == self.cells[-1].coord:
            self.__is_solved = True
            print('solved')
            return
        for d, direction in enumerate(self.nesw):
            can_go = True
            match d:
                case 0: # North
                    if current.north:
                        can_go = False
                case 1: # East
                    if current.east:
                        can_go = False
                case 2: # South
                    if current.south:
                        can_go = False
                case 3: # West
                    if current.west:
                        can_go = False
            if not can_go:
                continue
            next_coord = current.coord + direction
            idx = next_coord.y * self.colls + next_coord.x
            next_cell = self.cells[idx]
            if next_cell.closed:
                continue
            if not self.__open_set_has_cell(next_cell):
                next_node = Node(next_cell)
                next_node.parent = current_node
                self.__open_set.append(next_node)

    def __open_set_has_cell(self, cell: Cell):
        for node in self.__open_set:
            if node.cell.coord == cell.coord:
                return True
        return False

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
        current: Node = self.__head
        while current is not None:
            parent = current.parent
            if parent is None:
                break
            self.__win.draw_line(Line(current.cell.center, parent.cell.center), fill_color='green')
            current = parent
