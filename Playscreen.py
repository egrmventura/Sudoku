import pygame as pg
pg.font.init()

class Grid():
    dboard = [
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
    #rows = 9
    #cols = 9
    def __init__(self, win, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.win = win

    def draw_grid(self):
        gap = min(self.width/self.cols, self.height/self.rows)
        for i in range(min(self.rows,self.cols)+1):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(self.win, (0,0,0), (0,i * gap), (self.width, i * gap), thick)
            pg.draw.line(self.win, (0,0,0), (i * gap, 0), (i * gap, self.height), thick)



def redraw(win, board):
    win.fill((255,255,255))
    board.draw_grid()
    
def main():
    win = pg.display.set_mode((540,540))
    win.fill((240,240,240))
    pg.display.set_caption("Test")
    board = Grid(win, 540, 540, 9, 9)
    key = None
    run = True
    redraw(win, board)
    
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        redraw(win, board)
        pg.display.flip()
    
main()

