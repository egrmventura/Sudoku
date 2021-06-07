import pygame as pg
import time

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

#class Board:
#    def __init__(self, rows, cols, open = True):
#        pass
def fill_in(board, row, col):
    if find_blank(board)[0] == 9 and find_blank(board)[1] == 9:
        return True
    for i in range(1,10):
        if test_val(board,row, col, i):
            board[row][col] = i
            if fill_in(board, find_blank(board)[0], find_blank(board)[1]):
                return True
            board[row][col] = 0
    return False    

def find_blank(board):
    for row in range(0,9):
        for col in range(0,9):
            if board[row][col] == 0:
                return row, col
    return 9, 9

def test_val(board, row, col, val):
    #test along row
    for i in range(0, 9):
        if board[row][i] == val:
            return False
    #test along column
    for i in range(0,9):
        if board[i][col] == val:
            return False
    #test in 3x3 sections
    rowSection = row // 3
    colSection = col // 3
    for i in range(rowSection * 3, (rowSection+1) * 3):
        for j in range(colSection * 3, (colSection +1) * 3):
            if board[i][j] == val:
                return False
    
    return True
def print_board(board):
    fill_in(board, find_blank(board)[0], find_blank(board)[1])
    for i in range(0,9):
        print(board[i])

for i in range(0,9):
    print(demoboard[i])
print("Before : After")
print_board(demoboard)
