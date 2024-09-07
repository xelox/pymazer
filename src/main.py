from window import Window
from maze import Maze

def main():
    width = 800
    heigth = 600
    win = Window(width, heigth)
    maze = Maze(win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
