import time
from tkinter import Tk, Canvas
from line import Line

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.canvas.pack(fill='both', expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__update_callbacks = {}
        self.__update_timeout = 0

    def bind_key(self, key, callback):
        self.__root.bind(key, callback)

    def set_update_timeout(self, timeout):
        self.__update_timeout = timeout

    def add_update_callback(self, key, func):
        self.__update_callbacks[key] = func

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
            for callback in self.__update_callbacks.values():
                callback()
            time.sleep(self.__update_timeout)


    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color='black'):
        line.draw(self.canvas, fill_color=fill_color)
