#from Sudoku_proto import find_blank
import threading
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
    '''

    demoboard = [
        [0, 0, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 0, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 0, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 0, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 0]
    ]
    '''
    def __init__(self, rows, cols, width, height, win, section):
        self.rows = rows
        self.cols = cols
        self.section = section
        self.cubes = [[Cube(self.demoboard[i][j], i, j, width, height, 0) for j in range(cols)] for i in range(rows)]
        self.back_cubes = [[Cube(self.demoboard[i][j], i, j, width, height, 1) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.test_board = None
        self.update_test()
        self.backtest_board = None
        self.update_backtest()
        self.selected = None    #model is used as internal demo for testing
        self.win = win
        self.step_0 = 0
        self.step_1 = 0
    
    def update_test(self):
        self.test_board = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def update_backtest(self):
        self.backtest_board = [[self.back_cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set(value)
        self.back_cubes[row][col].set(value)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0: 
                if self.section == 0 and i == 0:
                    thick = 1
                #elif i != 9 and self.section != 0:
                #    thick = 1
                else:
                    thick = 4
            else:
                thick = 1
            pg.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pg.draw.line(self.win, (0,0,0), (i*gap, 0), (i*gap, self.width), thick)
            #print("height " + str(self.height))
            #print("y at " + str(((self.height - self.width) + (i*gap))))
            pg.draw.line(self.win, (0,0,0), (0, ((self.height - self.width) + (i*gap))), (self.width, ((self.height - self.width) + (i*gap))), thick)
            pg.draw.line(self.win, (0,0,0), (i* gap, self.height - self.width), (i*gap, self.height), thick)
    
        for i in range(self.rows):
            for j in range(self.cols):
                a = 0
                self.cubes[i][j].draw(self.win)
                self.back_cubes[i][j].draw(self.win)
    
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

    def backcheck_solve(self):
        test_cube = find_empty(self.backtest_board)
        if not test_cube:
            return True
        row, col = test_cube
        for num in range(9, 0, -1):
            if val_test(self.backtest_board, num, test_cube):
                self.backtest_board[row][col] = num
                if self.backcheck_solve():
                    return True
                self.backtest_board[row][col] = 0

        return False

    def GUI_solve(self):
        test_cube = find_empty(self.test_board)
        #backtest_cube = find_empty(self.backtest_board)
        #Forward test and backward test finished
        if not test_cube: # and not backtest_cube:
            return True
        #Backward test finished
        row, col = test_cube
        for num in range(1, 10):
            if val_test(self.test_board, num, test_cube):
                self.test_board[row][col] = num
                self.cubes[row][col].set(num)
                self.cubes[row][col].cube_update(self.win, True)
                self.update_test()
                pg.display.update()
                pg.time.delay(2)

                if self.GUI_solve():
                    return True

                self.test_board[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_test()
                self.cubes[row][col].cube_update(self.win, False)
                pg.display.update()
                pg.time.delay(2)
        
        return False

    def GUI_back_solve(self):
        backtest_cube = find_empty(self.backtest_board)
        #backtest_cube = find_empty(self.backtest_board)
        #Forward test and backward test finished
        if not backtest_cube: # and not backtest_cube:
            return True
        #Backward test finished
        row, col = backtest_cube
        for num in range(9, 0, -1):
            if val_test(self.backtest_board, num, backtest_cube):
                self.backtest_board[row][col] = num
                self.back_cubes[row][col].set(num)
                self.back_cubes[row][col].cube_update(self.win, True)
                self.update_backtest()
                pg.display.update()
                pg.time.delay(2)

                if self.GUI_back_solve():
                    return True

                self.backtest_board[row][col] = 0
                self.back_cubes[row][col].set(0)
                self.update_backtest()
                self.back_cubes[row][col].cube_update(self.win, False)
                pg.display.update()
                pg.time.delay(2)
        
        return False

    def update_board(self): #temp test for solve display
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].value = self.test_board[i][j]
                self.back_cubes[i][j].value = self.backtest_board[i][j]
    

class Cube:
    def __init__(self, value, row, col, width, height, section):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.value = value
        self.temp = 0
        self.selected = False
        self.cube_size = width / 9
        self.xzero = 0
        self.yzero = 0 if section == 0 else self.height - self.width
        self.section = section

    def draw(self, playboard):
        fnt = pg.font.SysFont("comic sans", 30)
        
        x = self.xzero + (self.col * self.cube_size)
        y = self.yzero + (self.row * self.cube_size)
        
#Reset this layout for showing upper and lower tests
        if self.value == 0 and self.temp != 0:
            text = fnt.render(str(self.temp), True, (128,128,128))
            playboard.blit(text, (x+3, y+3))
        elif self.value != 0:
            text = fnt.render(str(self.value), True, (0,0,0))
            playboard.blit(text, (x + (self.cube_size/2 - text.get_width()/2), y + (self.cube_size/2 - text.get_height()/2)))

        if self.selected:
            pg.draw.rect(playboard, (255,0,0), (x, y, self.cube_size, self.cube_size), 3)
    
    def cube_update(self, playboard, confirmed = True):
        fnt = pg.font.SysFont("comic sans", 30)
        x = (self.col * self.cube_size) + self.xzero
        y = (self.row * self.cube_size) + self.yzero

        pg.draw.rect(playboard, (255,255,255), (x, y, self.cube_size, self.cube_size), 0)

        text = fnt.render(str(self.value), 1, (0,0,0))
        playboard.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
        if confirmed:
            pg.draw.rect(playboard, (0,255,0), (x, y, self.cube_size, self.cube_size), 3)
        else:
            pg.draw.rect(playboard, (255,0,0), (x, y, self.cube_size, self.cube_size), 3)
    
    
    def set(self, num):
        self.value = num
    
    def temp_set(self, num):
        self.temp_value = num


def redraw_window(window, demoboard):
    window.fill((255,255,255))
    demoboard.draw()
    #add section number to the grid.draw()?


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

if __name__ == "__main__":
    win = pg.display.set_mode((360,750))
    pg.display.set_caption("Demo")
    board = Grid(9,9,360,750, win, 0)
    #board_backup = Grid(9,9,360,750, win, 1)
    key = None
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    
                    forward = threading.Thread(target= board.GUI_solve)
                    backward = threading.Thread(target= board.GUI_back_solve)
                
                    forward.start()
                    backward.start()

        redraw_window(win, board)
        pg.display.flip()
    
#main()