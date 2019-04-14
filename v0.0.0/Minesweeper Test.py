import pygame
import numpy as np
import numpy.random as rand


class grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        
        self.cellwidth = width/cols
        self.cellheight = height/rows
        
        self.minecells = []
        self.cellnumbers = []
        
        
        matrix = np.zeros((self.rows, self.cols)) #pointer array 
        k = -1
        num = 0
        for i in range(self.rows):
            for k in range(self.cols):
                matrix[i,k] = num
                num += 1
        self.cellpointer = matrix
        
        self.cell_list = []
        for i in range(int(matrix[-1][-1] + 1)):
            self.cell_list.append(i)
        
        
        self.visicells = [False]*len(self.cell_list)
    def drawgrid(self):
        for i in range(0, self.cols + 1):
            pointA = [i*self.cellwidth, 0]
            pointB = [i*self.cellwidth, self.height]
            pointC = [0, i*self.cellheight]
            pointD = [self.width, i*self.cellheight]
            pygame.draw.line(gameDisplay, (255, 255, 255), pointA, pointB)
            pygame.draw.line(gameDisplay, (255, 255, 255), pointC, pointD)
    
    def populatemines(self, mines):
        
        for cell in self.cell_list:
            if rand.random() <= mines/(self.cell_list[-1] - cell):
                self.minecells.append(cell)
                mines = mines - 1
                if mines == 0:
    
                    break
    def index_restrict(self, row, col):
        rowmin = row - 1
        rowmax = row + 2
        colmin = col - 1
        colmax = col + 2
        
        if rowmin < 0:
            rowmin = 0
        if rowmax > self.rows - 1:
            rowmax = self.rows 
        if colmin < 0:
            colmin = 0
        if colmax > self.cols - 1:
            colmax = self.cols
        
        return int(rowmin), int(rowmax), int(colmin), int(colmax)
    
            
    
    def set_cell_numbers(self):
        for cell in self.cell_list:
            row = np.where(self.cellpointer == cell)[0]
            col = np.where(self.cellpointer == cell)[1]
            
            num = 0
            
            rowmin, rowmax, colmin, colmax = self.index_restrict(row, col)
            
            for i in range(rowmin, rowmax):
                
                for k in range(colmin, colmax):
                    if self.cellpointer[i][k] in self.minecells:
                        num += 1
            self.cellnumbers.append(num)
            
    
    
    def set_cell_numbers_test(self, row, col):
        
            #row = np.where(self.cellpointer == cell)[0]
            #col = np.where(self.cellpointer == cell)[1]
            
           
            
        rowmin, rowmax, colmin, colmax = self.index_restrict(row, col)
        for i in range(rowmin, rowmax):
            for k in range(colmin, colmax):
                
                if self.cellpointer[i][k] in self.minecells:
                    x = 4
                           
            
    def drawmines(self):      
                
            #####
        for cell in self.cell_list:
            if cell in self.minecells:
                row = np.where(self.cellpointer == cell)[0]
                col = np.where(self.cellpointer == cell)[1]
                #xcoord = col*self.cellwidth + cellwidth/2
                #ycoord = row*self.cellheight + cellheight/2
                xcoord = col*self.cellwidth 
                ycoord = row*self.cellheight 
                pygame.draw.rect(gameDisplay, (205, 205, 205), (xcoord, ycoord, self.cellwidth, self.cellheight))
        
    def drawnumbers(self):
        colors = [(0, 0, 0), (0, 0, 255), (0, 127, 0), (255, 0, 0), (0, 0, 128), (134, 0, 0), (0, 128, 128), (255, 255, 255), (128, 128, 128)]
        
        for cell in self.cell_list:
            if cell not in self.minecells and self.visicells[self.cell_list.index(cell)] == True:
                row = np.where(self.cellpointer == cell)[0]
                col = np.where(self.cellpointer == cell)[1]
                #xcoord = col*self.cellwidth + cellwidth/2
                #ycoord = row*self.cellheight + cellheight/2
                xcoord = col*self.cellwidth 
                ycoord = row*self.cellheight 
                
                cellindex = self.cell_list.index(cell)
                string = str(self.cellnumbers[cellindex])
                
                color = colors[int(self.cellnumbers[cellindex])]
                
                textsurface = myfont.render(string, False, color)
                gameDisplay.blit(textsurface,(xcoord + self.cellwidth/3, ycoord + self.cellheight/5))

    def clickedcell(self, row, col):
        row, col = int(row), int(col)
        if self.cellpointer[row][col] in self.minecells:
            return True
        else:
            cell = self.cellpointer[row][col]
            cellindex = self.cell_list.index(cell)
            self.visicells[cellindex] = True
            
            
        

pygame.init()
clock = pygame.time.Clock()
width = 800
height = 600



gameDisplay = pygame.display.set_mode((width, height)) #creates display
pygame.display.set_caption("title") #sets title


pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textsurface = myfont.render('Some Text', False, (255, 255, 255))

mygrid = grid(16, 16, width, height)

mygrid.populatemines(50)
mygrid.set_cell_numbers()
fps = 60
running = True
drawmines = False
while running:


    gameDisplay.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                    
                
                   
                  pos = pygame.mouse.get_pos()
                  cellX = pos[0]/mygrid.cellwidth
                  cellY = pos[1]/mygrid.cellheight
                  
                  if mygrid.clickedcell(cellY, cellX) == True:
                      drawmines = True
                      break
                  
                  print(str(int(cellX)) + "|" + str(int(cellY)))
                  mygrid.set_cell_numbers_test(cellY, cellX)

    clock.tick(fps)
    mygrid.drawgrid()
    
    if drawmines == True:
        mygrid.drawmines()
    
    
    #gameDisplay.blit(textsurface,(0,0))
    mygrid.drawnumbers()
    pygame.display.update()
    
    



pygame.quit()