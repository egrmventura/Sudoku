import tkinter as ui
import time
import pygame as pg

class Cube:
    def __init__(self, row, col, width, height, val, permanent_val):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.permanent_val = permanent_val
        if permanent_val != 0:
            self.val = permanent_val
        else:
            self.val = val
