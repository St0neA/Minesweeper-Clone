import pygame
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt



class cell:
    def __init__(self, id, row, col, maxrow, maxcol, cellpointer):
        self.sprite = tile
        
        self.number = 0
        self.mine = False
        self.drawnum = False
        self.id = id
        self.clicked = False
        self.row = row
        self.col = col
        self.cellpointer = cellpointer
        
        self.adjacentIDs = []
        ##define adjacent
        for i in range(col - 1, col + 2):
            for k in range(row - 1, row + 2):
                
                r = k
                c = i
                
                if k < 0:
                    r = 0
                if k > maxrow:
                    r = maxrow
                if i < 0:
                    c = 0
                if i > maxcol:
                    c = maxcol
                
                r, c = int(r), int(c)
                cellID = cellpointer[r][c]
                self.adjacentIDs.append(cellID)
        self.adjacentIDs = list(set(self.adjacentIDs))
        
    def set_number(self):
        for cell in self.adjacentIDs:
            if cell.mine == True:
                self.number += 1
    def on_clicked(self, sprite = None):
        self.sprite = None
        self.clicked = True
        self.drawnum = True
        if self.mine == True:
            return True
        else:
            return False
        if sprite:
            self.sprite = sprite
    
    
class grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        
        self.cellwidth = width/cols
        self.cellheight = height/rows
        
        self.cells = []
        
        matrix = np.zeros((self.rows, self.cols)) #pointer array 
        k = -1
        num = 0
        for i in range(self.rows):
            for k in range(self.cols):
                matrix[i,k] = num
                num += 1
        self.cellpointer = matrix
        
        
    
        
        for i in range(rows*cols):
            row = np.where(self.cellpointer == i)[0][0]
            col = np.where(self.cellpointer == i)[1][0]
            ncell = cell(i, row, col, self.rows - 1, self.cols - 1, self.cellpointer)
            self.cells.append(ncell)

    def drawgrid(self):
        for i in range(0, self.cols + 1):
            pointA = [i*self.cellwidth, 0]
            pointB = [i*self.cellwidth, self.height]
            pointC = [0, i*self.cellheight]
            pointD = [self.width, i*self.cellheight]
            pygame.draw.line(gameDisplay, (255, 255, 255), pointA, pointB)
            pygame.draw.line(gameDisplay, (255, 255, 255), pointC, pointD)
        
    def populatemines(self, mines):
        
        for cell in self.cells:
            if rand.random() <= mines/(len(self.cells) - cell.id):
                cell.mine = True
                mines = mines - 1
                if mines == 0:
                    break
    def set_cell_numbers(self):
        for cell in self.cells:
            
            for adjacentID in cell.adjacentIDs:
                if self.cells[int(adjacentID)].mine == True:
                    cell.number += 1
        
    def showmines(self):
        
        for cell in self.cells:
            if cell.mine == True:
                
                gameDisplay.blit(mine, [cell.col*self.cellwidth, cell.row*self.cellheight]) 
    def drawnumbers(self):
            colors = [(0, 0, 0), (0, 0, 255), (0, 127, 0), (255, 0, 0), (0, 0, 128), (134, 0, 0), (0, 128, 128), (255, 255, 255), (128, 128, 128)]
            
            for cell in self.cells:
                if cell.drawnum == True and cell.mine == False:
                    
                    string = str(cell.number)
                    color = colors[int(cell.number)]
                    
                    textsurface = myfont.render(string, False, color)
                    gameDisplay.blit(textsurface,(cell.col*self.cellwidth + self.cellwidth/3, cell.row*self.cellheight + self.cellheight/5))

    def reveal(self):
        for cell in mygrid.cells:
            if cell.clicked == True and cell.number == 0:
                for adj in cell.adjacentIDs:
                    self.cells[int(adj)].drawnum = True
                    self.cells[int(adj)].sprite = None
                    if self.cells[int(adj)].number == 0:
                        self.cells[int(adj)].clicked = True
            
    #

    def draw_cell_sprites(self):
        for cell in self.cells:
            if cell.sprite:
                gameDisplay.blit(cell.sprite, [cell.col*self.cellwidth, cell.row*self.cellheight]) 

                        
pygame.init()
clock = pygame.time.Clock()
width = 800
height = 800
gameDisplay = pygame.display.set_mode((width, height)) #creates display
pygame.display.set_caption("title") #sets title


mine = pygame.image.load('minesprite.png').convert_alpha()
#    gameDisplay.blit(mine, [200, 200])    
tile = pygame.image.load('tilesprite.png').convert_alpha()
flagged = pygame.image.load("flagged.png").convert_alpha()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 20)


gameover = False
mygrid = grid(16, 16, 800, 800)
mygrid.populatemines(30)
mygrid.set_cell_numbers()
fps = 60
running = True
count = 0
while running:
    
    gameDisplay.fill((100,100,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                  pos = pygame.mouse.get_pos()
                  cellcol = pos[0]/mygrid.cellwidth
                  cellrow = pos[1]/mygrid.cellheight
                  ID = mygrid.cellpointer[int(cellrow)][int(cellcol)]
                  gameover = mygrid.cells[int(ID)].on_clicked()
                  
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] == 1:
            
            pos = pygame.mouse.get_pos()
            cellcol = pos[0]/mygrid.cellwidth
            cellrow = pos[1]/mygrid.cellheight
            ID = mygrid.cellpointer[int(cellrow)][int(cellcol)]
            sprite = mygrid.cells[int(ID)].sprite
            if mygrid.cells[int(ID)].sprite == tile:
                mygrid.cells[int(ID)].sprite = flagged
            elif sprite == flagged:
                mygrid.cells[int(ID)].sprite = tile

                
            

            
    mygrid.drawgrid()
    
    
    mygrid.draw_cell_sprites()
    if gameover == True:
        mygrid.showmines()
    mygrid.drawnumbers()
    if count == 5:
        mygrid.reveal()
        count = 0
        
    clock.tick(fps)
    pygame.display.update()
    count +=1
    
pygame.display.quit


pygame.quit()
exit()