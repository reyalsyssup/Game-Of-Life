import pygame
import uuid
pygame.init()

screenDimensions = (800, 600)
display = pygame.display.set_mode(screenDimensions)
run = True

cells = []

class Cell:
    def __init__(self, alive, neighbours, ID):
        self.alive = alive
        self.neighbours = neighbours
        self.ID = ID

class Grid:
    def setCellSize(size=20):
        offset = size/16
        size = screenDimensions[0]/size/2-offset
        return (offset, size)
    def initCells():
        global cells
        cells = list(range(int(screenDimensions[1]/20)))
        cell = Cell(False, [], uuid.uuid4())
        for i in range(len(cells)):
            cells[i] = list(range(int(screenDimensions[0]/20)))
            for j in range(len(cells[i])):
                cells[i][j] = cell
    def renderCells():
        display.fill((255,255,255))
        x,y = 0,0
        for i in cells:
            for j in i:
                if j.alive: pygame.draw.rect(display, (255,255,255), (x+Grid.setCellSize()[0], y+Grid.setCellSize()[0], Grid.setCellSize()[1], Grid.setCellSize()[1]))
                else: pygame.draw.rect(display, (0,0,0), (x+Grid.setCellSize()[0], y+Grid.setCellSize()[0], Grid.setCellSize()[1], Grid.setCellSize()[1]))
                y+=20
            y=0; x+=20
    def updateCells(row, spot):
        cells[row][spot].alive = False
    
Grid.initCells()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            pass

    Grid.renderCells()
    Grid.updateCells(0, 0)
    pygame.display.update()
        
"""
Live cells:

1. a live cell with zero or one live neighbours will die.
2. a live cell with two or three live neighbours will remain alive
3. a live cell with four or more live neighbours will die.
Dead cells:

1. a dead cell with exactly three live neighbours becomes alive
2. in all other cases a dead cell will stay dead.
"""   