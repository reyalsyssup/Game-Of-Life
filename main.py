import pygame, copy, pickle, os, sys
pygame.init()

# I wouldnt reccomend changing this :)
screenDimensions = (800, 600)
display = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("Game of Life")
display.set_alpha(None)
run = True
game = False

cells = []

class Cell():
    def __init__(self, alive, neighbours, x, y, size, hovered):
        self.alive = alive
        self.neighbours = neighbours
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
    def renderCell(self, x, y, alive):
        self.alive = alive
        if self.alive: color = (255,255,255)
        else: color = (0,0,0)
        if self.hovered: color = (255,255,0)
        x+=1; y+=1
        renderedCell = pygame.draw.rect(display, color, (x, y, 19, 19))
        return renderedCell
    def setNeighbours(self):
        total = 0
        me = [(ix,iy) for ix, row in enumerate(cells) for iy, i in enumerate(row) if i == self][0]
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
            LM = cells[me[0]-1][me[1]]
            if LM.alive: total += 1
        except: pass
        try:
            RM = cells[me[0]+1][me[1]]
            if RM.alive: total += 1
        except: pass
        self.neighbours = total
    def updateSurroundingNeighbours(self):
        me = [(ix,iy) for ix, row in enumerate(cells) for iy, i in enumerate(row) if i == self][0]
        # # # # # # # CORNERS # # # # # # # #
        try: 
            TR = cells[me[0]+1][me[1]-1]
            TR.setNeighbours()
        except: pass
        try: 
            BR = cells[me[0]+1][me[1]+1]
            BR.setNeighbours()
        except: pass
        try: 
            TL = cells[me[0]-1][me[1]-1]
            TL.setNeighbours()
        except: pass
        try:
            BL = cells[me[0]-1][me[1]+1]
            BL.setNeighbours()
        except: pass

        # # # # # # # # # # # EDGES # # # # # # # # # # #
        try: 
            TM = cells[me[0]][me[1]-1]
            TM.setNeighbours()
        except: pass
        try: 
            BM = cells[me[0]][me[1]+1]
            BM.setNeighbours()
        except: pass
        try: 
            LM = cells[me[0]-1][me[1]]
            LM.setNeighbours()
        except: pass
        try:
            RM = cells[me[0]+1][me[1]]
            RM.setNeighbours()
        except: pass
                        
cell = Cell(False, 0, 0, 0, 0, False)

class Grid:
    def initCells():
        global cells
        cells = list(range(int(screenDimensions[0]/20)))
        for i in range(len(cells)):
            cells[i] = list(range(int(screenDimensions[1]/20)))
            for j in range(len(cells[i])):
                cells[i][j] = copy.deepcopy(cell)
    def renderCells():
        if not game: display.fill((255,0,0))
        else: display.fill((0,255,0))
        x,y = 0,0
        cellsToChange = []
        for i in cells:
            for j in i:
                j.x = x; j.y = y
                j.size = 19
                # # # # # # # GAME RULES # # # # # # #
                if game:
                    if j.alive and (j.neighbours == 2 or j.neighbours == 3): 
                        cellsToChange.append((j, True))
                    if j.alive and (j.neighbours != 2 and j.neighbours != 3):
                        cellsToChange.append((j, False))
                    if j.alive == False and j.neighbours == 3: 
                        cellsToChange.append((j, True))
                j.renderCell(x, y, j.alive)
                j.checkHover()
                y+=20
            y=0; x+=20
        if game:
            for i in cellsToChange:
                i[0].alive = i[1]
                i[0].setNeighbours()
                i[0].updateSurroundingNeighbours()

Grid.initCells()
while True:
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                cellLoc = None
                if event.button == 1:
                    for i in cells:
                        for j in i:
                            if j.checkHover():
                                j.alive = not j.alive
                                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for i in cells:
                        for j in i:
                            j.setNeighbours()
                    run = not run; game = not game
                if event.key == pygame.K_r:
                    for i in cells:
                        for j in i: j.alive = False
                if event.key == pygame.K_s:
                    for i in cells:
                        for j in i:
                            j.setNeighbours()
                    i = 0
                    while os.path.exists("./saves/save%s.pickle" % i):
                        i+=1
                    pickleOut = open("./saves/save%s.pickle" % i, "wb")
                    pickle.dump(cells, pickleOut)
                    pickleOut.close()
                if event.key == pygame.K_l:
                    i = 0
                    try: i = sys.argv[1]
                    except:
                        i = 0
                        while os.path.exists("./saves/save%s.pickle" % i):
                            i+=1
                        i-=1
                    pickleIn = open("./saves/save%s.pickle" % i, "rb")
                    cells = pickle.load(pickleIn)
                    pickleIn.close()
        
        Grid.renderCells()
        pygame.display.update() 

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = not run; game = not game
        Grid.renderCells()
        pygame.display.update()