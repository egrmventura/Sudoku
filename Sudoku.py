#from Sudoku_proto import find_blank
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
        self.test_board = None
        self.update_test()
        self.selected = None    #model is used as internal demo for testing
        self.win = win
    
    def update_test(self):
        self.test_board = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

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
    
    def solve(self):
        test_cube = find_empty(self.test_board)
        if not test_cube:
            return True
        row, col = test_cube
        for num in range(1, 10):
            if val_test(self.test_board, num, test_cube):
                self.test_board[row][col] = num
                if self.solve():
                    return True
                self.test_board[row][col] = 0

        return False

    def update_board(self): #temp test for solve display
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].value = self.test_board[i][j]


    

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

        if self.selected:
            pg.draw.rect(playboard, (255,0,0), (x, y, self.cube_size, self.cube_size), 3)


def redraw_window(window, demoboard):
    window.fill((255,255,255))
    demoboard.draw()

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)   #row, col of empty

def val_test(board, num, pos):
    row = pos[0]
    col = pos[1]
    row_sect = row // 3
    col_sect = col // 3
    for i in range(len(board[0])):  #check along row
        if board[row][i] == num and i != col:
            return False
    
    for i in range(len(board)):    #check along column
        if board[i][col] == num and i != row:
            return False
    
    for i in range(row_sect * 3, (row_sect * 3) + 3):
        for j in range(col_sect * 3, (col_sect * 3) +3):
            if board[i][j] == num and i != row and j != col:
                return False
    
    return True #passed all tests

def main():
    win = pg.display.set_mode((540,600))
    pg.display.set_caption("Demo")
    board = Grid(9,9,540,540, win)
    key = None
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    board.solve()
                    board.update_board()


        redraw_window(win, board)
        pg.display.flip()
    
main()