from window import Window
from point import Point
from cell import Cell

def main():
    width = 800
    heigth = 600
    win = Window(width, heigth)
    cells = []
    for x in range(0, width, Cell.size):
        for y in range(0, heigth, Cell.size):
            cell = Cell(win, Point(x, y))
            cells.append(cell)
            cell.draw()
    win.wait_for_close()


if __name__ == "__main__":
    main()
