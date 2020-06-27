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
from pygame.locals import *
import uuid
import copy
pygame.init()
# Increases efficiency apparently
flags = DOUBLEBUF
pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])

# I wouldnt reccomend chaning this :)
screenDimensions = (800, 600)
display = pygame.display.set_mode(screenDimensions, flags)
display.set_alpha(None)
run = True

cells = []

class Cell():
    def __init__(self, alive, neighbours, ID, x, y, size, hovered):
        self.alive = alive
        self.neighbours = neighbours
        self.ID = ID
        self.x = x
        self.y = y
        self.size = size
        self.hovered = hovered
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
        renderedCell = pygame.draw.rect(display, color, (x+Grid.setCellSize()[0], y+Grid.setCellSize()[0], Grid.setCellSize()[1], Grid.setCellSize()[1]))
        return renderedCell
cell = Cell(False, [], "", 0, 0, 0, False)

class Grid:
    def setCellSize(size=20):
        offset = 1.25
        totalSpace = size
        size = screenDimensions[0]/size/2-offset
        return (offset, size, totalSpace)
    def initCells():
        global cells
        cells = list(range(int(screenDimensions[1]/Grid.setCellSize()[2])))
        for i in range(len(cells)):
            cells[i] = list(range(int(screenDimensions[0]/Grid.setCellSize()[2])))
            for j in range(len(cells[i])):
                # MUST COPY BECAUSE OTHER WISE IT IS THE EXACT, THE EXACTT FUCKING SAME DICTIONARY (or class now ig) FUCK YOU PYTHON YOU STUPID PIECE OF SHIT KYS FAG
                cells[i][j] = copy.deepcopy(cell)
                cells[i][j].ID = str(uuid.uuid4())
    def renderCells():
        display.fill((255,255,255))
        x,y = 0,0
        for i in cells:
            for j in i:
                j.x = x; j.y = y
                j.size = Grid.setCellSize()[1]
                j.renderCell(x, y)
                y+=Grid.setCellSize()[2]
            y=0; x+=Grid.setCellSize()[2]
    
Grid.initCells()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            for i in cells:
                for j in i:
                    if j.checkHover():
                        j.alive = not j.alive
    
    for i in cells:
        for j in i:
            j.checkHover()

    
    Grid.renderCells()
    pygame.display.update() 