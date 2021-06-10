import tkinter as ui
import time
import pygame as pg

demoboard = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

#class Grid:
#    def __init__(self, row, col, wid)


class Cube:
    def __init__(self, row, col, width, height, value, permanent_val):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.permanent_val = permanent_val
        if permanent_val != 0:
            self.value = permanent_val
        else:
            self.value = value
        self.temp = 0
        self.selected = False
        self.cube_size = width / 9

    def draw(self, playboard):
        font = pg.font.SysFont("comic sans", 46)
        
        x = self.col * self.cube_size
        y = self.row * self.cube_size

        if self.value == 0 and self.temp != 0:
            text = font.render(str(self.temp), True, (128,128,128))
            playboard.blit(text, (x+5, y+5))
        else:
            text = font.render(str(self.value), True, (0,0,0))
            playboard.blit(text, (x + (self.cube_size/2 - text.get_width()/2), y + (self.cube_size/2 - text.get_height()/2)))

        if self.selected:
            pg.draw.rect(playboard, (255,0,0), (x, y, self.cube_size, self.cube_size))



