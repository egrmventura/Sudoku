#from Sudoku_proto import find_blank
import threading
import math
import random
import time
import pygame as pg
from icecream import ic
pg.font.init()

class Grid:
    '''    
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
    
    demoboard = [
        [0, 0, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 0, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 0, 0, 3, 0, 0, 0, 1, 2],
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
    
    forcount = 0
    bakcount = 0

    def __init__(self, width, height, win):
        self.width = width
        self.height = height
        self.play_gap = 0
        self.test_gap = 0
        self.board_dimensions()
        self.play_cubes = [[Cube(self.demoboard[i][j], i, j, width, height, self.play_gap, 0) for j in range(9)] for i in range(9)]
        self.test_cubes = [[Cube(self.demoboard[i][j], i, j, width, height, self.test_gap, 1) for j in range(9)] for i in range(9)]
        self.backtest_cubes = [[Cube(self.demoboard[i][j], i, j, width, height, self.test_gap, 2) for j in range(9)] for i in range(9)]
        self.play_board = None
        self.update_playboard()
        self.test_board = None
        self.update_test()
        self.backtest_board = None
        self.update_backtest()
        self.selected = None    #model is used as internal demo for testing
        self.win = win
        self.test_status = None
        self.opening_strikes = 5
    
    def update_playboard(self):
        self.play_board = [[self.play_cubes[i][j].value for j in range(9)] for i in range(9)]

    def update_test(self):
        self.test_board = [[self.test_cubes[i][j].value for j in range(9)] for i in range(9)]

    def update_backtest(self):
        self.backtest_board = [[self.backtest_cubes[i][j].value for j in range(9)] for i in range(9)]
    
    # TODO create dimensions of play and test boards in with 1:1.4 ratio, leaving gap between them with rounded of mutliples
    def board_dimensions(self):
        # TODO 860 x 620 with 60x60 and 33x33 with gaps. Check if gaps should be increased and become part of influence of dimensions
        if self.height / 17 <= self.width / 22:
            self.test_gap = self.height // 20
            self.play_gap = math.ceil((self.width - (10 *  self.test_gap))/9)
            ic("a", self.play_gap, self.test_gap, self.height, self.width)
        else:
            self.play_gap = math.ceil((self.width // 22) * 1.5)
            self.test_gap = math.ceil((self.width - (9 * self.play_gap))/10)
            ic("b", self.play_gap, self.test_gap)

    def sketch(self, value):    
        # TODO check into use of sketch function and whether to separate for different cube classes
        row, col = self.selected
        self.play_cubes[row][col].set(value)
        self.test_cubes[row][col].set(value)
        self.backtest_cubes[row][col].set(value)

    def draw(self):
        for i in range(10):
            if i % 3 == 0: 
                thick = 4
            else:
                thick = 1
            #play board - first: horizontal, second: vertical
            pg.draw.line(self.win, (0,0,0), (0, i * self.play_gap), (9 * self.play_gap, i * self.play_gap), thick)
            pg.draw.line(self.win, (0,0,0), (i * self.play_gap, 0), (i * self.play_gap, 9 * self.play_gap), thick)
            #test board
            pg.draw.line(self.win, (0,0,0), ((self.width - (9 * self.test_gap)), i * self.test_gap), (self.width, i * self.test_gap), thick)
            pg.draw.line(self.win, (0,0,0), (self.width - ((9 - i) * self.test_gap), 0), (self.width - ((9 - i) * self.test_gap), 9 * self.test_gap), thick)
            #backtest board
            pg.draw.line(self.win, (0,0,0), (self.width - (9 * self.test_gap), self.height - ((9 - i) * self.test_gap)), (self.width, self.height - ((9 - i) * self.test_gap)), thick)
            pg.draw.line(self.win, (0,0,0), (self.width - ((9 - i) * self.test_gap), self.height - (9 * self.test_gap)), (self.width - ((9 - i) * self.test_gap), self.height), thick)
    
        for i in range(9):
            for j in range(9):
                # TODO alter CUBE draw function for playboard
                self.play_cubes[i][j].draw(self.win)
                self.test_cubes[i][j].draw(self.win)
                self.backtest_cubes[i][j].draw(self.win)

        # TODO alter Valid/Invalid status style and location
        fnt = pg.font.SysFont("comic sans", 40)
        if self.test_status == True:
            text = fnt.render("VALID PUZZLE", True, (90, 150, 55))
            pg.draw.rect(self.win, (190, 220, 170), (0, self.width, self.width, self.height - (2 * self.width)))
            self.win.blit(text, ((self.width - text.get_width())/ 2, (self.height - text.get_height()) / 2))
            
        elif self.test_status == False:
            text = fnt.render("INVALID PUZZLE", True, (200, 45, 0))
            pg.draw.rect(self.win, (240, 160, 160), (0, self.width, self.width, self.height - (2 * self.width)))
            self.win.blit(text, ((self.width - text.get_width())/ 2, (self.height - text.get_height()) / 2))
            
    
    def solve(self, board, forward=True):
        test_cube = find_empty(board)
        if not test_cube:
            return True
        row, col = test_cube
        if forward:
            for num in range(1, 10):
                if val_test(board, num, test_cube):
                    board[row][col] = num
                    if self.solve(board, True):
                        return True
                    board[row][col] = 0
        else:
            for num in range(9, 0, -1):
                if val_test(board, num, test_cube):
                    board[row][col] = num
                    if self.solve(board, False):
                        return True
                    board[row][col] = 0

        return False

    def GUI_solve(self):
        test_cube = find_empty(self.test_board)
        if not test_cube:
            return True
        row, col = test_cube
        for num in range(1, 10):
            if val_test(self.test_board, num, test_cube):
                self.test_board[row][col] = num
                self.test_cubes[row][col].set(num)
                self.test_cubes[row][col].cube_update(self.win, True)
                self.update_test()
                pg.display.update()
                time.sleep(.005)
                if self.GUI_solve():
                    return True

                self.test_board[row][col] = 0
                self.test_cubes[row][col].set(0)
                self.update_test()
                self.test_cubes[row][col].cube_update(self.win, False)
                pg.display.update()
                time.sleep(.005)
        return False

    def GUI_back_solve(self):
        backtest_cube = find_empty(self.backtest_board)
        if not backtest_cube:
            return True
        row, col = backtest_cube
        for num in range(9, 0, -1):
            if val_test(self.backtest_board, num, backtest_cube):
                self.backtest_board[row][col] = num
                self.backtest_cubes[row][col].set(num)
                self.backtest_cubes[row][col].cube_update(self.win, True)
                self.update_backtest()
                pg.display.update()
                self.bakcount+=1
                time.sleep(.005)
                if self.GUI_back_solve():
                    return True

                self.backtest_board[row][col] = 0
                self.backtest_cubes[row][col].set(0)
                self.update_backtest()
                self.backtest_cubes[row][col].cube_update(self.win, False)
                pg.display.update()
                self.bakcount+=1
                time.sleep(.005)
        return False

    # TODO reevaluate "update_board". Either apply a variable for play vs test or create 2nd function
    def update_board(self): #temp test for solve display
        for i in range(9):
            for j in range(9):
                self.test_cubes[i][j].value = self.test_board[i][j]
                self.backtest_cubes[i][j].value = self.backtest_board[i][j]
    
    #correct_test checks the forward and backward tests to find if they are the same 
    #if they are not the same, then there is more than one answer answer to the sudoku
    def correct_test(self): 
        for i in range(9):
            for j in range(9):
                if self.test_cubes[i][j].value != self.backtest_cubes[i][j].value:
                    self.test_cubes[i][j].cube_update(self.win, True, False)
                    self.backtest_cubes[i][j].cube_update(self.win, True, False)
                    self.test_cubes[i][j].draw(self.win)
                    self.backtest_cubes[i][j].draw(self.win)
                    print("incorrect at [" + str(i) + "][" + str(j) + "]")
                    self.test_status = False
        
        if not (self.test_status == False):
            self.test_status = True
    
    def correct_test_bool(self):
        cube_removal_test_for = self.test_board
        cube_removal_test_back = self.backtest_board
        self.solve(cube_removal_test_for)
        self.solve(cube_removal_test_back, False)
        for i in range(9):
            for j in range(9):
                if cube_removal_test_for[i][j] != cube_removal_test_back[i][j]:
                    return False
        return True

    def clear_cubes(self):
        for i in range(9):
            for j in range(9):
                self.play_cubes[i][j].set(0)
                self.play_cubes[i][j].temp_set(0)
                self.play_cubes[i][j].cube_update(self.win)
                self.test_cubes[i][j].set(0)
                self.test_cubes[i][j].temp_set(0)
                self.test_cubes[i][j].cube_update(self.win)
                self.backtest_cubes[i][j].set(0)
                self.backtest_cubes[i][j].temp_set(0)
                self.backtest_cubes[i][j].cube_update(self.win)
        self.update_playboard()
        self.update_test()
        self.update_backtest()
        pg.display.update()

    def board_dup(self): #Duplicates test boards from play board
        for i in range(9):
            for j in range(9):
                self.test_board[i][j] = self.play_board[i][j]
                self.backtest_board[i][j] = self.play_board[i][j]

    def random_fill(self):
        fill_cube = find_empty(self.play_board)
        if not fill_cube:
            self.board_dup()
            return True
        row, col = fill_cube
        numlist = [1,2,3,4,5,6,7,8,9]
        random.shuffle(numlist)
        for num in numlist:
            if val_test(self.test_board, num, fill_cube):
                self.test_board[row][col] = num
                if self.random_fill():
                    return True
                self.test_board[row][col] = 0
        return False
    
    def GUI_random_fill(self):
        fill_cube = find_empty(self.play_board)
        if not fill_cube:
            self.board_dup()
            pg.display.update()
            return True
        row, col = fill_cube
        numlist = [1,2,3,4,5,6,7,8,9]
        random.shuffle(numlist)
        for num in numlist:
            if val_test(self.play_board, num, fill_cube):
                self.play_board[row][col] = num
                self.play_cubes[row][col].set(num)
                self.play_cubes[row][col].cube_update(self.win, True)
                self.update_playboard()
                pg.display.update()
                time.sleep(0.005)
                if self.GUI_random_fill():
                    return True
                
                self.play_board[row][col] = 0
                self.play_cubes[row][col].set(0)
                self.play_cubes[row][col].cube_update(self.win, False)
                self.update_playboard()
                pg.display.update()
                time.sleep(0.005)
        return False

    def remove_opening(self): ###Not working yet.
        if self.opening_strikes <= 0:
            return True
        for _ in range(5):
            row1, col1, row2, col2 = open_cube_coord()
            temp_val1, temp_val2 = self.test_board[row1][col1], self.test_board[row2][col2]
            if temp_val1 == 0 and temp_val2 ==0:
                return False
            else:
                self.test_board[row1][col1], self.test_board[row2][col2] = 0, 0
                self.backtest_board[row1][col1], self.backtest_board[row2][col2] = 0, 0
                ic(row1, col1, temp_val1, row2, col2, temp_val2)
                
            
                ic(self.opening_strikes, self.test_board, self.backtest_board)
                if self.correct_test_bool():
                    if self.remove_opening():
                        return True
                ic("Fail, repopulate")
                self.opening_strikes-=1
                self.test_board[row1][col1], self.test_board[row2][col2] = temp_val1, temp_val2
                self.backtest_board[row1][col1], self.backtest_board[row2][col2] = temp_val1, temp_val2
        return False
            



        
        


class Cube:
    def __init__(self, value, row, col, width, height, cube_size, section):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.value = value
        self.temp = 0
        self.selected = False
        self.cube_size = cube_size
        #sections: 0 = playboard, 1 = forward testboard, 2 = backward testboard
        self.section = section
        #xzero is 0 is playboard, or 9-cube offset from width if testboard
        self.xzero = 0 if section == 0 else self.width - (9 * self.cube_size)
        #yzero is 9-cube offset from bottom if backward testboard, and 0 for playboard and forward testboard
        self.yzero = self.height - (9 * self.cube_size) if section == 2 else 0
        
        self.cube_status = True

    def draw(self, playboard):
        fnt = pg.font.SysFont("comic sans", math.ceil(0.75 * self.cube_size))
        
        x = self.xzero + (self.col * self.cube_size)
        y = self.yzero + (self.row * self.cube_size)
        

        if not self.cube_status:
            pg.draw.rect(playboard, (240, 160, 160), (x, y, self.cube_size, self.cube_size))
            text = fnt.render(str(self.value), 1, (200, 45, 0))
            playboard.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
        else:
            if self.value == 0 and self.temp != 0:
                text = fnt.render(str(self.temp), True, (128,128,128))
                playboard.blit(text, (x+3, y+3))
            elif self.value != 0:
                text = fnt.render(str(self.value), True, (0,0,0))
                playboard.blit(text, (x + (self.cube_size/2 - text.get_width()/2), y + (self.cube_size/2 - text.get_height()/2)))

            if self.selected:
                pg.draw.rect(playboard, (200, 45, 0), (x, y, self.cube_size, self.cube_size), 3)
    
    # TODO reevaluate confirmed vs correct use. May be outdated. Make 0 at Newboard blank
    def cube_update(self, playboard, confirmed = True, correct = True):
        fnt = pg.font.SysFont("comic sans", math.ceil(0.75 * self.cube_size))
        x = (self.col * self.cube_size) + self.xzero
        y = (self.row * self.cube_size) + self.yzero
        self.cube_status = correct
        

        if not self.cube_status:
            pg.draw.rect(playboard, (240, 160, 160), (x, y, self.cube_size, self.cube_size))
            text = fnt.render(str(self.value), 1, (200, 45, 0))
            playboard.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
        else:
            pg.draw.rect(playboard, (255, 255, 255), (x, y, self.cube_size, self.cube_size), 0)
            text = fnt.render(str(self.value), 1, (0,0,0))
            playboard.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
            if confirmed:
                pg.draw.rect(playboard, (90, 150, 55), (x, y, self.cube_size, self.cube_size), 3)
            else:
                pg.draw.rect(playboard, (200, 45, 0), (x, y, self.cube_size, self.cube_size), 3)
        
            
        
        
    
    
    def set(self, num):
        self.value = num
    
    def temp_set(self, num):
        self.temp_value = num


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

def GUI_output(board):
    '''while not (find_empty(board.backtest_board) == None) and not (find_empty(board.test_board) == None):
        forward = threading.Thread(target= board.GUI_solve)
        forward.start()
        #forward.join()
        #time.sleep(0.001)
        backward = threading.Thread(target= board.GUI_back_solve)
    
        #forward.start()
        backward.start()
        forward.join()
        backward.join()
    '''
    board.GUI_solve()
    board.GUI_back_solve()
    board.correct_test()

def randomfill(board):
    board.clear_cubes()
    board.random_fill()
    board.update_board()
    pg.display.update()
    
def open_board_cubes(board):
    board.remove_opening()
    board.update_board()
    pg.display.update()

def remove_cubes(board):
    board.remove_opening()
    board.update_board()
    pg.display.update()

def open_cube_coord():
    row1 = random.randint(0,8)
    col1 = random.randint(0,8)
    mirr = random.randint(0,3)
    #mirr is mirror axis [ 0:y-axis, 1:y=x axis, 2:x-axis, 3:y=-x axis ]
    if mirr == 0:
        return([row1, col1, row1, 8-col1])
    elif mirr == 1:
        return([row1, col1, col1, row1])
    elif mirr == 2:
        return([row1, col1, 8-row1, col1])
    else:
        return([row1, col1, 8-col1, 8-row1])

def GUIrandfill(board):
    board.clear_cubes()
    pg.display.update()
    board.GUI_random_fill()    

if __name__ == "__main__":
    win_width = 880
    win_height = 680
    win = pg.display.set_mode((win_width,win_height))
    #Playboard  = 540 x 540, Test Boards = 306 x 306
    pg.display.set_caption("Demo")
    board = Grid(win_width,win_height, win)
    #board_backup = Grid(9,9,360,750, win, 1)
    key = None
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    GUI_output(board)
                
                if event.key == pg.K_m:
                    randomfill(board)
                    time.sleep(4)
                    open_board_cubes(board)
                
                if event.key == pg.K_n:
                    GUIrandfill(board)

                if event.key == pg.K_r:
                    remove_cubes(board)
                    
                '''solve print of validity / test false match'''

        redraw_window(win, board)
        pg.display.flip()
    
#main()