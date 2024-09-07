from tkinter import Canvas
from point import Point

class Line: # pylint: disable=too-few-public-methods
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def draw(self, canvas: Canvas, fill_color='black', width=2):
        canvas.create_line(
            self.a.x,
            self.a.y,
            self.b.x,
            self.b.y,
            fill=fill_color,
            width=width
        )
