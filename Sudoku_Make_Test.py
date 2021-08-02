#from Sudoku_proto import find_blank
import threading
import math
import random
import time
import pygame as pg
from icecream import ic
pg.font.init()

class Grid:
    
    forcount = 0
    bakcount = 0
    #TODO 7/29 PM read below notes
    '''
    Current layout does not have a trigger of testing the guess input against the answer.
    Set a hidden matrix with the solution to check when answered along with the reformatting if there are invalid guesses.
    Set the temp_val inputs to input value if new with highlight, highlight existing if typed, remove if delete is hit, and set to full if enter is hit in guessing process (maybe actuall temp_val?)
    Reform the program for the temp values and perm values around the 3rd note; this will have a large impact on already written code.
    '''
    def __init__(self, width, height, win, puzzle, puzzle_solving = True):
        self.width = width
        self.height = height
        self.play_gap = 0
        self.test_gap = 0
        self.board_dimensions()
        self.play_cubes = [[Cube(puzzle[i][j], i, j, width, height, self.play_gap, 0) for j in range(9)] for i in range(9)]
        self.puzzle_solving = puzzle_solving
        if self.puzzle_solving:
            self.test_cubes = [[Cube(0, i, j, width, height, self.test_gap, 1) for j in range(9)] for i in range(9)]
            self.backtest_cubes = [[Cube(0, i, j, width, height, self.test_gap, 2) for j in range(9)] for i in range(9)]
        else:
            self.test_cubes = [[Cube(puzzle[i][j], i, j, width, height, self.test_gap, 1) for j in range(9)] for i in range(9)]
            self.backtest_cubes = [[Cube(puzzle[i][j], i, j, width, height, self.test_gap, 2) for j in range(9)] for i in range(9)]
        self.play_board = None
        self.update_playboard()
        self.test_board = None  #test_board is used for testing on puzzle writing and solution model on puzzle solving
        self.update_test()
        self.backtest_board = None
        self.update_backtest()
        self.selected = None
        self.win = win
        #TODO 7/29 PM apply guess_status to set sketch boundaries for updates and formating with temp_val displays
        self.guess_status = None
        self.test_status = None
        self.opening_strikes = 3
    
    def update_playboard(self):
        self.play_board = [[self.play_cubes[i][j].value for j in range(9)] for i in range(9)]

    def update_test(self):
        self.test_board = [[self.test_cubes[i][j].value for j in range(9)] for i in range(9)]

    def update_backtest(self):
        self.backtest_board = [[self.backtest_cubes[i][j].value for j in range(9)] for i in range(9)]
    
    def board_dimensions(self):
        #General ratio of 1.8:1 for play board to test board on window
        if self.height / 17 <= self.width / 22:
            self.test_gap = self.height // 20
            self.play_gap = math.ceil((self.width - (10 *  self.test_gap))/9)
        else:
            self.play_gap = math.ceil((self.width // 22) * 1.5)
            self.test_gap = math.ceil((self.width - (9 * self.play_gap))/10)

    def sketch(self, num, guess_change = False, guess_bool = True):    
        # TODO 8/1 add additional parameters for the guessing num or adding to guess array
        row, col = self.selected
        if guess_change:
            if not guess_bool:
                num = self.play_cubes[row][col].guess
                self.play_cubes[row][col].guess_set(0)
            else:    
                self.play_cubes[row][col].guess_set(num)
            self.identical_cube(num, guess_bool)
        else:
            self.play_cubes[row][col].temp_set(num)
        if not self.puzzle_solving:
            self.test_cubes[row][col].temp_set(num)
            self.backtest_cubes[row][col].temp_set(num)

    # TODO 8/1 update the dup and dup_count uses througout the play_cubes
    def identical_cube(self, num, guess_bool):
    #find if matching values in cubes within row, col, and or section and adapt dup status
        row, col = self.selected
        row_sect = row // 3
        col_sect = col // 3
        for j in range(9):
            if self.play_cubes[row][j] == num and j != col:
                self.cube_dup_update(row, col, row, j, guess_bool)
                
        for i in range(9):
            if self.play_cubes[i][col] == num and i != row:
                self.cube_dup_update(row, col, i, col, guess_bool)
                
        for i in range(row_sect * 3, (row_sect * 3) + 3):
            for j in range(col_sect * 3, (col_sect * 3) +3):
                if board[i][j] == num and i != row and j != col:
                    self.cube_dup_update(row, col, i, j, guess_bool)

    def cube_dup_update(self, row1, col1, row2, col2, guess_bool):
        self.play_cubes[row1][col1].dup = guess_bool
        if not guess_bool:
            self.play_cubes[row2][col2].dup_count -= 1
            if self.play_cubes[row2][col2].dup_count == 0:
                self.play_cubes[row2][col2].dup = False
        else:
            self.play_cubes[row2][col2].dup_count += 1
            self.play_cubes[row2][col2].dup = True



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

    def select(self, row, col):
        for i in range(9):
            for j in range(9):
                self.play_cubes[i][j].selected = False
        
        self.play_cubes[row][col].selected = True
        self.selected = (row, col)
    
    #TODO 7/31 correct board.clear function. not clearing input values. May involve value/temp_val usage
    def clear(self):
        row, col = self.selected[0], self.selected[1]
        if self.play_cubes[row][col].value == 0:
            self.play_cubes[row][col].temp_set(0)

    def click(self, pos):
        if pos[0] < (9 * self.play_gap) and pos[1] < (9 * self.play_gap):
            x = pos[0] // self.play_gap
            y = pos[1] // self.play_gap
            return (int(y), int(x))
        else:
            return None
    
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
                time.sleep(.00025)
                if self.GUI_solve():
                    return True

                self.test_board[row][col] = 0
                self.test_cubes[row][col].set(0)
                self.update_test()
                self.test_cubes[row][col].cube_update(self.win, False)
                pg.display.update()
                time.sleep(.00025)
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
                time.sleep(.00025)
                if self.GUI_back_solve():
                    return True

                self.backtest_board[row][col] = 0
                self.backtest_cubes[row][col].set(0)
                self.update_backtest()
                self.backtest_cubes[row][col].cube_update(self.win, False)
                pg.display.update()
                self.bakcount+=1
                time.sleep(.00025)
        return False

    # TODO reevaluate "update_board". Either apply a variable for play vs test or create 2nd function
    def update_test_cubes(self): #temp test for solve display
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

    def board_dup(self): #Duplicates test boards from play board
        for i in range(9):
            for j in range(9):
                self.test_board[i][j] = self.play_board[i][j]
                self.backtest_board[i][j] = self.play_board[i][j]
    
    def board_cube_dup(self): #Duplicates test boards from play board
        for i in range(9):
            for j in range(9):
                self.test_board[i][j] = self.play_board[i][j]
                self.test_cubes[i][j].value = self.play_board[i][j]
                self.backtest_board[i][j] = self.play_board[i][j]
                self.backtest_cubes[i][j].value = self.play_board[i][j]
    
    def play_cube_dup(self):
        for i in range(9):
            for j in range(9):
                self.play_cubes[i][j].value = self.play_board[i][j]

    def random_fill(self):
        fill_cube = find_empty(self.play_board)
        if not fill_cube:
            self.board_dup()
            return True
        row, col = fill_cube
        numlist = [1,2,3,4,5,6,7,8,9]
        random.shuffle(numlist)
        for num in numlist:
            if val_test(self.play_board, num, fill_cube):
                self.play_board[row][col] = num
                if self.random_fill():
                    return True
                self.play_board[row][col] = 0
        return False
    
    def GUI_random_fill(self):
        fill_cube = find_empty(self.play_board)
        if not fill_cube:
            self.board_cube_dup()
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


    def make_puzzle(self): 
        if self.opening_strikes <= 0:
            return True
        
        for _ in range(max(1, self.opening_strikes)):
            
            temp_val1, temp_val2 = 0, 0
            while temp_val1 == 0 and temp_val2 == 0:
                row1, col1, row2, col2 = open_cube_coord()
                temp_val1, temp_val2 = self.play_board[row1][col1], self.play_board[row2][col2]
            self.puzzle_test(row1, col1, row2, col2)
            self.solve(self.test_board)
            self.solve(self.backtest_board, False)
            if self.correct_test_bool():
                self.puzzle_test(row1, col1, row2, col2, False)
                if self.make_puzzle():
                    return True
            
            self.opening_strikes-=1
            self.puzzle_test(row1, col1, row2, col2, False, False)
        return False

    def GUI_make_puzzle(self): 
        #ic(self.opening_strikes)
        if self.opening_strikes <= 0:
            return True
        
        for _ in range(max(1, self.opening_strikes)):
            
            #ic("strikes left", max(0,int(self.opening_strikes)))
            temp_val1, temp_val2 = 0, 0
            while temp_val1 == 0 and temp_val2 == 0:
                row1, col1, row2, col2 = open_cube_coord()
                temp_val1, temp_val2 = self.play_board[row1][col1], self.play_board[row2][col2]
            self.puzzle_test_formatting(row1, col1, row2, col2)
            self.GUI_solve()
            self.GUI_back_solve()
            
            if self.correct_test_bool():
                self.puzzle_test_formatting(row1, col1, row2, col2, False)
                if self.GUI_make_puzzle():
                    return True
            
            self.opening_strikes-=1
            self.puzzle_test_formatting(row1, col1, row2, col2, False, False)
        return False
    
    def puzzle_test(self, row1, col1, row2, col2, start = True, passed = True):
        # :start: start of the test, temporarily setting to 0
        # :passed: passed the test, cube at 0 has only 1 solution
        if row1 == row2 and col1 == col2:
            if start:
                self.board_dup()
                self.test_board[row1][col1], self.backtest_board[row1][col1] = 0, 0
            elif passed:
                self.play_board[row1][col1] = 0
            else:
                self.board_dup()
        
        else:
            if start:
                self.board_dup()
                self.test_board[row1][col1], self.backtest_board[row1][col1] = 0, 0
                self.test_board[row2][col2], self.backtest_board[row1][col1] = 0, 0
            elif passed:
                self.play_board[row1][col1], self.play_board[row2][col2] = 0, 0
            else:
                self.board_dup()
    
    def puzzle_test_formatting(self, row1, col1, row2, col2, start = True, passed = True):
        # :start: start of the test, temporarily setting to 0
        # :passed: passed the test, cube at 0 has only 1 solution
        if row1 == row2 and col1 == col2:
            if start:
                self.board_cube_dup()
                self.play_cubes[row1][col1].selected = True
                self.test_board[row1][col1], self.backtest_board[row1][col1] = 0, 0
                self.test_cubes[row1][col1].set(0)
                self.backtest_cubes[row1][col1].set(0)
                self.win.fill((255, 255, 255))
                self.draw()
                pg.display.update()
            elif passed:
                self.play_cubes[row1][col1].selected = False
                self.play_cubes[row1][col1].set(0)
                self.play_board[row1][col1] = 0
                self.win.fill((255, 255, 255))
                self.draw()
                pg.display.update()
            else:
                self.play_cubes[row1][col1].selected = False
                self.board_cube_dup()
                self.win.fill((255, 255, 255))
                self.draw()
                pg.display.update()
        
        else:
            if start:
                self.board_cube_dup()
                self.play_cubes[row1][col1].selected = True
                self.test_board[row1][col1], self.backtest_board[row1][col1] = 0, 0
                self.test_cubes[row1][col1].set(0)
                self.backtest_cubes[row1][col1].set(0)
                self.play_cubes[row2][col2].selected = True
                self.test_board[row2][col2], self.backtest_board[row1][col1] = 0, 0
                self.test_cubes[row2][col2].set(0)
                self.backtest_cubes[row2][col2].set(0)
                self.win.fill((255, 255, 255))
                self.draw()
                pg.display.update()
            elif passed:
                self.play_cubes[row1][col1].selected = False
                self.play_cubes[row1][col1].set(0)
                self.play_board[row1][col1] = 0
                self.play_cubes[row2][col2].selected = False
                self.play_cubes[row2][col2].set(0)
                self.play_board[row2][col2] = 0
                self.win.fill((255, 255, 255))
                self.draw()
                pg.display.update()
            else:
                self.play_cubes[row1][col1].selected = False
                self.play_cubes[row2][col2].selected = False
                self.board_cube_dup()
                self.win.fill((255, 255, 255))
                self.draw()
                pg.display.update()
    
    
            



        
        


class Cube:
    def __init__(self, value, row, col, width, height, cube_size, section):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        #TODO 8/1 track temp vs temp_val in code. Make sure temp is current selected value that can be add/removed from guess_vals or placed as guessed val
        #TODO 8/1 value is assigned as provided value in initial code, temp was for guess with intention of just Y/N correct.
        self.value = value
        #temp value is temporary imput that can be applied to guess_vals or as guess
        self.temp = 0
        #guess set to guessed value when solving
        self.guess = 0
        #TODO 7/29 set formatting in solving cubes for guess T/F and guess values On/Off
        #guess_vals status on 1-9 for temp guess values, shown on perimeter of cube
        self.guess_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.selected = False
        self.cube_size = cube_size
        #sections: 0 = playboard, 1 = forward testboard, 2 = backward testboard
        self.section = section
        self.dup = False
        self.dup_count = 0
        #xzero is 0 is playboard, or 9-cube offset from width if testboard
        self.xzero = 0 if section == 0 else self.width - (9 * self.cube_size)
        #yzero is 9-cube offset from bottom if backward testboard, and 0 for playboard and forward testboard
        self.yzero = self.height - (9 * self.cube_size) if section == 2 else 0


    def draw(self, board):
        fnt = pg.font.SysFont("comic sans", math.ceil(0.75 * self.cube_size))
        list_fnt = pg.font.SysFont("comic sans", math.ceil(0.2 * self.cube_size))
        x = self.xzero + (self.col * self.cube_size)
        y = self.yzero + (self.row * self.cube_size)
        

    
        #TODO 8/1 add dup status
        '''
        Each cube will be redrawn upon a key being pressed under current format.
        Evaluate whether isolating updates is faster or not.
        If it is, then update each Play_Cube to draw a box over the guess number(s) or the solid number.
        Be sure to put in the update of color for contradicting guesses or permanents.
        Also check the validity of the booleans and values for the temp system
        '''
        if self.value == 0 and self.guess != 0:
            if self.dup:
                # TODO 8/2 figure out how to lay down rectangle within grid lines
                pg.draw.rect(board, (240, 160, 160), (x, y, self.cube_size, self.cube_size))
            text = fnt.render(str(self.guess), True, (128, 128, 128))
            board.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
            
        elif self.value == 0 and self.temp != 0:
            
            print_pos = self.guess_num_offset()
            #TODO 7/29 - test updated guessing track
            if self.guess_vals[self.temp - 1] == 0:
                self.guess_vals[self.temp - 1] = self.temp
            else:
                self.guess_vals[self.temp - 1] = 0
            for i in range(9):
                if self.guess_vals[i] != 0:
                    text = list_fnt.render(str(self.guess_vals[i]), True, (128,128,128))
                    board.blit(text, (x + print_pos[i][0], y + print_pos[i][1]))
            
        elif self.value != 0:
            if self.dup:
                pg.draw.rect(board, (240, 160, 160), (x, y, self.cube_size, self.cube_size))
            text = fnt.render(str(self.value), True, (0,0,0))
            board.blit(text, (x + (self.cube_size/2 - text.get_width()/2), y + (self.cube_size/2 - text.get_height()/2)))

        if self.selected:
            pg.draw.rect(board, (200, 45, 0), (x, y, self.cube_size, self.cube_size), 3)

    def guess_num_offset(self):
        mini_cube_size = self.cube_size / 3
        list_fnt = pg.font.SysFont("comic sans", math.ceil(0.2 * self.cube_size))
        offset = []
        for i in range(9):
            text = list_fnt.render(str(i+1), True, (0,0,0))
            row_offset = ((i % 3) * mini_cube_size) + ((mini_cube_size - text.get_width()) / 2)
            col_offset = ((i // 3) * mini_cube_size) + ((mini_cube_size - text.get_height()) / 2)
            offset.append([row_offset, col_offset])
        return offset

    def cube_update(self, board, confirmed = True, correct = True):
        # :confirmed: whether or not cube value valid in backtracking algorithm
        # :correct: after test and back test fill in values for puzzle, any that do not match are False
        x = (self.col * self.cube_size) + self.xzero
        y = (self.row * self.cube_size) + self.yzero
        
        fnt = pg.font.SysFont("comic sans", math.ceil(0.75 * self.cube_size))
        if not correct: 
            pg.draw.rect(board, (240, 160, 160), (x, y, self.cube_size, self.cube_size))
            text = fnt.render(str(self.value), 1, (200, 45, 0))
            board.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
        else:
            pg.draw.rect(board, (255, 255, 255), (x, y, self.cube_size, self.cube_size), 0)
            text = fnt.render(str(self.value), 1, (0,0,0))
            board.blit(text, (x + ((self.cube_size - text.get_width())/2), y + ((self.cube_size - text.get_height())/2)))
            if confirmed:
                pg.draw.rect(board, (90, 150, 55), (x, y, self.cube_size, self.cube_size), 3)
            else:
                pg.draw.rect(board, (200, 45, 0), (x, y, self.cube_size, self.cube_size), 3)
        
    def set(self, num):
        self.value = num
    
    def guess_set(self, num):
        self.guess = num

    def temp_set(self, num):
        self.temp_value = num


def redraw_window(window, board):
    window.fill((255,255,255))
    board.draw()

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)   #row, col of empty

def val_test(board, num, pos):
    #find if matching values in cubes within row, col, and or section and return boolean
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

#TODO check on possible CUBE attribute to highlight matching value cells for error check



def open_cube_coord():
    #function to randomly select 2 cubes to test at 0 for new sudoku puzzle
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

def board_nums(name):
    if name == "demoboard":
        '''    
        puzzle = [
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
        
        puzzle = [
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

        puzzle = [
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

    else:

        puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    
    return puzzle



# TODO 7/29 set threading for simultanious appearance of GUI solve and back solve
if __name__ == "__main__":
    
    win_width = 880
    win_height = 680
    puzzle = board_nums("demoboard")
    win = pg.display.set_mode((win_width, win_height))
    #Window split: Play board  = 540 x 540, Test Boards = 306 x 306 each
    pg.display.set_caption("Demo")
    board = Grid(win_width, win_height, win, puzzle, True)
    key = None
    run = True
    guess_bool = False
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    board.GUI_solve()
                    board.GUI_back_solve()
                    board.correct_test()
                
                if event.key == pg.K_m:
                    puzzle = board_nums("clear")
                    board = Grid(win_width, win_height, win, puzzle, False)
                    redraw_window(win, board)
                    board.GUI_random_fill()
                    redraw_window(win, board)
                    pg.display.update()
                    board.GUI_make_puzzle()

                if event.key == pg.K_n:
                    puzzle = board_nums("clear")
                    board = Grid(win_width, win_height, win, puzzle, False)
                    redraw_window(win, board)
                    board.GUI_random_fill()

                if event.key == pg.K_r:
                    puzzle = board_nums("clear")
                    win.fill((255, 255, 255))
                    board = Grid(win_width, win_height, win, puzzle)
                
                
                if event.key == pg.K_p:
                    puzzle = board_nums("clear")
                    board = Grid(win_width, win_height, win, puzzle)
                    board.random_fill()
                    board.make_puzzle()
                    puzzle = board.play_board
                    board = Grid(win_width, win_height, win, puzzle, True)

                if event.key == pg.K_RETURN:
                    guess_bool = True

                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                
                #TODO setup deletion for solving inputs and puzzle creation inputs
                if event.key == pg.K_DELETE:
                    board.clear()
                    key = None
                
                '''solve print of validity / test false match'''
            
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key, True, guess_bool)
            guess_bool = False

        redraw_window(win, board)
        pg.display.flip()
    
#main()