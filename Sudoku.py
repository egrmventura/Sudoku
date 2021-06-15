import tkinter as ui
import time
import pygame as pg
pg.font.init()

class Grid:
    
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

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.demoboard[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None    #model is used as internal demo for testing
        self.win = win
    
    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set(value)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pg.draw.line(self.win, (0,0,0), (i*gap, 0), (i*gap, self.width), thick)
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

class Cube:
    def __init__(self, value, row, col, width, height):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.value = value
        self.temp = 0
        self.selected = False
        self.cube_size = width / 9

    def draw(self, playboard):
        fnt = pg.font.SysFont("comic sans", 46)
        
        x = self.col * self.cube_size
        y = self.row * self.cube_size

        if self.value == 0 and self.temp != 0:
            text = fnt.render(str(self.temp), True, (128,128,128))
            playboard.blit(text, (x+5, y+5))
        else:
            text = fnt.render(str(self.value), True, (0,0,0))
            playboard.blit(text, (x + (self.cube_size/2 - text.get_width()/2), y + (self.cube_size/2 - text.get_height()/2)))

        #if self.selected:
        #    pg.draw.rect(playboard, (255,0,0), (x, y, self.cube_size, self.cube_size))


def redraw_window(window, demoboard):
    window.fill((255,255,255))
    demoboard.draw()

def main():
    win = pg.display.set_mode((540,600))
    pg.display.set_caption("Demo")
    board = Grid(9,9,540,540, win)
    #key = None
    run = True
    while run:
        redraw_window(win, board)
    
main()