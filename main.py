"""
Live cells:

1. a live cell with zero or one live neighbours will die.
2. a live cell with two or three live neighbours will remain alive
3. a live cell with four or more live neighbours will die.
Dead cells:

1. a dead cell with exactly three live neighbours becomes alive
2. in all other cases a dead cell will stay dead.
"""  

import pygame
import copy
import uuid
pygame.init()

# I wouldnt reccomend changing this :)
screenDimensions = (600, 600)
display = pygame.display.set_mode(screenDimensions)
display.set_alpha(None)
run = True

cells = []

class Cell():
    def __init__(self, alive, neighbours, x, y, size, hovered, ID):
        self.alive = alive
        self.neighbours = neighbours
        self.x = x
        self.y = y
        self.size = size
        self.hovered = hovered
        self.ID = ID
    def checkHover(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.size and pos[1] > self.y and pos[1] < self.y + self.size:
            self.hovered = True
            return True
        else: self.hovered = False
    def renderCell(self, x, y):
        if self.alive: color = (255,255,255)
        else: color = (0,0,0)
        if self.hovered: color = (255,255,0)
        x+=1; y+=1
        renderedCell = pygame.draw.rect(display, color, (x, y, 19, 19))
        return renderedCell
    def setNeighbours(self):
        total = 0
        me = [(ix,iy) for ix, row in enumerate(cells) for iy, i in enumerate(row) if i == self][0]

        TR,BR,BL,TL = None,None,None,None
        TM,BM,LM,RM = None,None,None,None
        # # # # # # # CORNERS # # # # # # # #
        try: 
            TR = cells[me[0]+1][me[1]-1]
            if TR.alive: total += 1
        except: pass
        try: 
            BR = cells[me[0]+1][me[1]+1]
            if BR.alive: total += 1
        except: pass
        try: 
            TL = cells[me[0]-1][me[1]-1]
            if TL.alive: total += 1
        except: pass
        try:
            BL = cells[me[0]-1][me[1]+1]
            if BL.alive: total += 1
        except: pass

        # # # # # # # # # # # EDGES # # # # # # # # # # #
        try: 
            TM = cells[me[0]][me[1]-1]
            if TM.alive: total += 1
        except: pass
        try: 
            BM = cells[me[0]][me[1]+1]
            if BM.alive: total += 1
        except: pass
        try: 
            LR = cells[me[0]-1][me[1]]
            if LR.alive: total += 1
        except: pass
        try:
            RM = cells[me[0]+1][me[1]]
            if RM.alive: total += 1
        except: pass
        self.neighbours = total
                        
cell = Cell(False, 0, 0, 0, 0, False, "")

class Grid:
    def initCells():
        global cells
        cells = list(range(int(screenDimensions[1]/20)))
        for i in range(len(cells)):
            cells[i] = list(range(int(screenDimensions[0]/20)))
            for j in range(len(cells[i])):
                # MUST COPY BECAUSE OTHER WISE IT IS THE EXACT, THE EXACTT FUCKING SAME DICTIONARY (or class now ig) FUCK YOU PYTHON YOU STUPID PIECE OF SHIT KYS FAG
                cells[i][j] = copy.deepcopy(cell)
                cells[i][j].ID = str(uuid.uuid4())
        cells[1][1].alive = True
        for i in cells:
            for j in i:
                j.setNeighbours()
    def renderCells():
        display.fill((0,0,255))
        x,y = 0,0
        for i in cells:
            for j in i:
                j.x = x; j.y = y
                j.size = 18.75
                j.renderCell(x, y)
                j.checkHover()
                y+=20
            y=0; x+=20

Grid.initCells()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for i in cells:
                    for j in i:
                        if j.checkHover():
                            j.alive = not j.alive
                            break
                for i in cells:
                    for j in i:
                        j.setNeighbours()
    
    Grid.renderCells()
    print(f"cells[1][1] neighbours: {cells[1][1].neighbours}")
    pygame.display.update() 