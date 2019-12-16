import numpy as np
import time
from tkinter import *
from tkinter import ttk

# Window Class
class App(Tk):
    def __init__(self, *args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        #useful variables
        self.n = 20 # number of cells = n*n
        self.a = np.zeros((self.n, self.n))#array with cell information
        self.b = np.zeros((self.n, self.n))
        self.cells = {}#dictionary containing the visual cell objects
        self.running = True
        #Content Frame
        self.title('Game of Life')
        self.content = ttk.Frame(self, padding=(5))
        self.content.grid(row =0, column=0, sticky=(N,S,E,W))
        #Cells Frame
        self.canvas = Canvas(self.content, width=500, height=500,
                borderwidth=0, highlightthickness=0,
                background='white')
        self.canvas.grid(row=0, column=0, sticky=(N,S,E,W))
        self.canvas.bind('<Configure>', self.draw)
        #Controls Frame and buttons
        self.controls = ttk.Frame(self.content, padding=(5))
        self.controls.grid(row=1, column=0, sticky=(N,S,E,W))
        self.start = ttk.Button(self.controls, text='Start',
                command=self.start_game)
        self.start.grid(row=0, column=0, sticky=(W))
        self.stop = ttk.Button(self.controls, text='Stop',
                command=self.stop_game)
        self.stop.grid(row=0, column=2, sticky=(E))
        self.random = ttk.Button(self.controls, text='random',
                command=self.randgen)
        self.random.grid(row=0, column=1, sticky=(E,W))
        #Size Configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=4)
        self.content.rowconfigure(1, weight=1)
        self.controls.columnconfigure(0,weight=1)
        self.controls.columnconfigure(1,weight=1)
        self.controls.columnconfigure(2,weight=1)
        self.controls.rowconfigure(0,weight=1)

    def draw(self, event=None):
        #Draws the grid with the cells
        self.canvas.delete('rect')
        width = int(self.canvas.winfo_width()/self.n)
        height = int(self.canvas.winfo_height()/self.n)
        for col in range(self.n):
            for row in range(self.n):
                x1 = col*width
                x2 = x1 + width
                y1 = row*height
                y2 = y1 + height
                if self.a[row][col]==0:
                    cell = self.canvas.create_rectangle(x1, y1, x2, y2,
                            fill='white', tags='cell')
                else:
                    cell = self.canvas.create_rectangle(x1, y1, x2, y2,
                            fill='black', tags='cell')
                self.cells[row, col] = cell
                self.canvas.tag_bind(cell, '<Button-1>', lambda event,
                        row=row, col=col: self.click(row, col))

    def click(self, row, col):
        #Changes the value and color of a cell when is clicked
        cell = self.cells[row,col]
        color = 'white' if self.a[row, col] == 1. else 'black'
        if self.a[row,col] == 0:
            self.a[row, col]=1
        else:
            self.a[row,col]=0
        self.canvas.itemconfigure(cell, fill=color)

    def game(self):
        #Decides if a cell is born, dies or stays alive
        self.draw()
        time.sleep(.1)
        if self.running: 
            for row in range(self.n):
                for col in range(self.n):
                    cell = self.cells[row,col]
                    neighbors = self.neighbors(row, col)
                    if self.a[row, col] == 0. and neighbors == 3.:
                        self.b[row, col] = 1.
                    elif self.a[row, col] == 1. and (neighbors==2. \
                       or neighbors==3.):
                        self.b[row, col]=1.    
                    else:
                        self.b[row, col]==0.
            self.a = self.b
            self.b = np.zeros((self.n,self.n))
            self.after(1, self.game)

    def start_game(self):
        #Changes the value of running and calls game()
        self.running = True
        self.game()

    def stop_game(self):
        #changes the value of runnung to stop game()'s loop
        self.running = False

    def neighbors(self,row,col):
        #Counts the alive neighbor cells
        if row != 0 and row != self.n -1 and col != 0 \
         and col != self.n-1:
            count = self.a[row-1, col-1] + self.a[row-1, col] + self.a[row-1, col+1] \
                 + self.a[row, col-1] + self.a[row, col+1] \
                 + self.a[row+1, col-1] + self.a[row+1, col] + self.a[row+1, col+1]
        elif row ==0 and col ==0:
            count = self.a[row, col+1] + self.a[row+1, col] + self.a[row+1, col+1]
        elif row==0 and col==self.n-1:
            count = self.a[row, col-1] + self.a[row+1, col-1] + self.a[row+1, col]
        elif row==self.n-1 and col==0:
            count = self.a[row-1, col] + self.a[row-1, col+1] + self.a[row, col+1]
        elif row==self.n-1 and col==self.n-1:
            count = self.a[row-1,col-1] + self.a[row-1, col] + self.a[row, col-1]
        elif row == 0:
            count = self.a[row, col-1] + self.a[row, col+1] \
                    + self.a[row+1, col-1] + self.a[row+1, col] + self.a[row+1, col+1]
        elif row == self.n-1:
            count = self.a[row-1, col-1] + self.a[row-1, col] + self.a[row-1, col+1] \
                    + self.a[row, col-1] + self.a[row, col+1]
        elif col == 0:
            count = self.a[row-1, col] + self.a[row-1, col+1] \
                    + self.a[row, col+1] \
                    + self.a[row+1, col] + self.a[row+1, col+1]
        elif col == self.n-1:
            count = self.a[row-1, col-1] + self.a[row-1, col] \
                    + self.a[row, col-1] \
                    + self.a[row+1, col-1] + self.a[row+1, col]
        return count

    def randgen(self):
        n = self.n
        cellstogen = np.random.randint(0, int(n*n/2))
        self.b = np.zeros((n, n))
        for cell in range(cellstogen):
            i = np.random.randint(0, n-1)
            j = np.random.randint(0, n-1)
            self.b[i,j] = 1
        self.a = self.b
        self.draw()


if __name__ == '__main__':
    gameoflife = App()
    gameoflife.mainloop()
