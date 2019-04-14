import pygame
import numpy as np
import numpy.random as rand
import os

#controls mines/flags remaining sprites
def mine_digits(num): #take num and convert into three digits
    global digits
    
    num = str(num)
    
    if len(num) == 2:
        num = "0" + num
    elif len(num) == 1:
        num = "00" + num

      
    dig1 = digits[int(num[0])]
    dig2 = digits[int(num[1])]
    dig3 = digits[int(num[2])]
    
    sprites = [dig1, dig2, dig3]
    dignum = 0
    for i in range(0, 13*3, 13):
        
        gameDisplay.blit(sprites[dignum], (17 + i, 17))
        dignum += 1
    
#controls counter digits
def counter_digits(num):
    
    global digits
    num = int(num)
    num = str(num)
    
    if len(num) == 2:
        num = "0" + num
    elif len(num) == 1:
        num = "00" + num
     
    dig1 = digits[int(num[0])]
    dig2 = digits[int(num[1])]
    dig3 = digits[int(num[2])]
    sprites = [dig1, dig2, dig3]
    dignum = 0
    for i in range(13*3, 0, -13):
        
        gameDisplay.blit(sprites[dignum], (width -(17 + 13 + i), 17))
        dignum += 1
        
    return

#draws border of the game
def draw_border():
    #oh dear
    global height
    global width
    global banner_height
    
    #left side
    pygame.draw.rect(gameDisplay, (255, 255, 255), pygame.Rect(0, 0, 3, height)) #outer white (left)
    pygame.draw.rect(gameDisplay, (192, 192, 192), pygame.Rect(3, 3, 6, height)) #middle grey
    pygame.draw.rect(gameDisplay, (128, 128, 128), pygame.Rect(9, 3, 3, height- 9)) #right darker grey
    
    #bottom
    pygame.draw.rect(gameDisplay, (192, 192, 192), pygame.Rect(3, height - 5, width - 3, 5))
    
    #right side
    pygame.draw.rect(gameDisplay, (192, 192, 192), pygame.Rect(width - 5, 0, 5, height))
    
    #banner
    pygame.draw.rect(gameDisplay, (192, 192, 192), pygame.Rect(3, 3, width, banner_height))
    
    #top
    pygame.draw.rect(gameDisplay, (128, 128, 128), pygame.Rect(9, banner_height -3, width - 5 - 12 + 3, 3))


#revealing function for "flipped cells"
def reveal(cells): #it's over for flipped cells
    for cell in cells: 
        if cell.flipped == True and cell.number == 0: #flip adjacents
            for adj in cell.adjacentIDs: 
                cells[int(adj)].flipped = True
                
#                if cells[int(adj)].number == 0: #pretty sure this isn't needed
#                    cells[int(adj)].flipped = True

#fill grid with mines
def populatemines(mines, clearspace): #takes point clicked which CANNOT be a mine
    global cells
    for cell in cells:
        #if random number (0-1) is less than remaining_mines/remaining cells
        #this means if the remaining_mines is to high or the remaning cells is too small, it increases probability
        if rand.random() <= mines/(len(cells) - cell.id) and cell.id != clearspace:
            cell.mine = True
            mines = mines - 1
            if mines == 0:
                break

    for cell in cells:
        cell.set_number(cells)
    

class cell: 
    def __init__(self, id, row, col, maxrow, maxcol):
        
        self.cellwidth = 16
        self.cellheight = 16
        self.row = row
        self.col = col
        
        self.cellpointer = np.zeros((int(maxrow + 1), int(maxcol + 1))) #np array to get cellID with row and col coordinate
        num = 0
        for i in range(maxrow + 1):
            for k in range(maxcol + 1):
                self.cellpointer[i,k] = num
                num += 1
        
        self.sprite = blanktile
        
        self.number = 0
        
        self.mine = False
        self.flipped = False
        self.id = id
        
        self.adjacentIDs = []
        ##define adjacent
        for i in range(col - 1, col + 2):
            for k in range(row - 1, row + 2):
                
                r = k #row and col
                c = i
                
                #restricts adjacent cells to those on grid
                if k < 0: 
                    r = 0
                if k > maxrow:
                    r = maxrow
                if i < 0:
                    c = 0
                if i > maxcol:
                    c = maxcol
                
                r, c = int(r), int(c)
                cellID = self.cellpointer[r][c] #finds adjacent cellID
                self.adjacentIDs.append(cellID) #adds to list
                
        self.adjacentIDs = list(set(self.adjacentIDs)) #deletes duplicate values
        
        
    def on_left_click(self): #left click handling
      
        self.flipped = True #flips
        if self.mine == True: #sets redmine sprite if applicable and reveals all mines
            for cell in cells: 
                if cell.mine == True:
                    cell.sprite = minesprite
            self.sprite = clickedmine
            return True #returns gameover
        else:
            self.set_sprite() 
            return False #returns gameover
        
    
    def on_right_click(self, flagnum): #right click handling
        
        #if no flags left and cell clicked isn't flagged, return
        if flagnum == 0 and self.sprite != flaggedtile: 
            return
        
        #changes sprite
        if self.sprite == blanktile:
            self.sprite = flaggedtile
        elif self.sprite == flaggedtile:
            self.sprite = blanktile
            
            
    def set_number(self, cells): #counts number of adjacent mines
        for adj in self.adjacentIDs:
            if cells[int(adj)].mine == True:
                self.number += 1
        
        
    def set_sprite(self): #sets the sprite
        if self.flipped == True and self.mine == False:
            self.sprite = numtiles[int(self.number)]
        
                    
    def draw(self): #draws cell
        gameDisplay.blit(self.sprite, [self.col*self.cellwidth + left_border, self.row*self.cellheight + banner_height])
    
            
    
gamerows = 16
gamecols = 16
minenum = 40
pygame.init()

banner_height = 53

bottom_border = 8
left_border = 12
right_border = 8


#set clock and window dimensions
clock = pygame.time.Clock() 
width = 16*gamecols + left_border + right_border
height = 16*gamerows + bottom_border + banner_height


gameDisplay = pygame.display.set_mode((width, height)) #creates display
pygame.display.set_caption("Minesweeper") #sets title

skin = "XPsprites"
os.chdir(skin)

clickedmine = pygame.image.load('clickedmine.png').convert_alpha() #load sprites
minesprite = pygame.image.load('mine.png').convert_alpha() 
blanktile = pygame.image.load('blanktile.png').convert_alpha()
flaggedtile = pygame.image.load("flaggedtile.png").convert_alpha()
numtiles = [
        pygame.image.load("0tile.png").convert_alpha(),
        pygame.image.load("1tile.png").convert_alpha(),
        pygame.image.load("2tile.png").convert_alpha(),
        pygame.image.load("3tile.png").convert_alpha(),
        pygame.image.load("4tile.png").convert_alpha(),
        pygame.image.load("5tile.png").convert_alpha(),
        pygame.image.load("6tile.png").convert_alpha(),
        pygame.image.load("7tile.png").convert_alpha(),
        pygame.image.load("8tile.png").convert_alpha()
        ]
digits = [
        pygame.image.load("0.png").convert_alpha(),
        pygame.image.load("1.png").convert_alpha(),
        pygame.image.load("2.png").convert_alpha(),
        pygame.image.load("3.png").convert_alpha(),
        pygame.image.load("4.png").convert_alpha(),
        pygame.image.load("5.png").convert_alpha(),
        pygame.image.load("6.png").convert_alpha(),
        pygame.image.load("7.png").convert_alpha(),
        pygame.image.load("8.png").convert_alpha(),
        pygame.image.load("9.png").convert_alpha()

        ]

fps = 60
running = True

def create_cells(rows, cols):
    cells = []
    id = 0
    for row in range(rows):
        for col in range(cols):
            cells.append(cell(id, row, col, rows-1, cols-1))
            id += 1
        
    return cells
        

cells = create_cells(gamerows, gamecols)


flagnum = minenum
gameover = False
gamewin = False
gamestart = False

def main(): 
    #OH DEAR
    global running
    global gameover
    global cells
    global gamerows
    global gamecols
    global minenum
    global height
    global width
    global left_border
    global right_border
    global banner_height
    global flagnum
    global gamewin
    global gamestart
    
    start_ticks=pygame.time.get_ticks()
    while running: #main loop
        
        if gameover == True:
            print("You lost!")
            endcount = pygame.time.get_ticks()
            while True:
                clock.tick(fps)
                endsecs = (pygame.time.get_ticks()-endcount)/1000
                if endsecs > 3:
                    running = False
                    break
        
        
        
        ####background
        gameDisplay.fill((255,255,255))
        draw_border()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
                
                
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()
                cellcol = int((pos[0] - left_border)/16)
                cellrow = int((pos[1] - banner_height)/16)
                
                
                if cellcol in range(0, gamecols) and cellrow in range(gamerows): #checks if on grid
                     
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                          #finds cell ID and calls on_left_clicked
                          pos = pygame.mouse.get_pos()
                          cellcol = (pos[0] - left_border)/16
                          cellrow = (pos[1] - banner_height)/16
                          ID = cells[0].cellpointer[int(cellrow)][int(cellcol)]
                          
                          gameover = cells[int(ID)].on_left_click() #also checks if gameover
                          
                          if gamestart == False: #if game hasn't started yet
                              gamestart = True
                              populatemines(minenum, ID) #fill mines and start counter
                              start_ticks=pygame.time.get_ticks()
        
        
                    #right click
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] == 1:
                          pos = pygame.mouse.get_pos()
                          cellcol = (pos[0] - left_border)/16
                          cellrow = (pos[1] - banner_height)/16
                          ID = cells[0].cellpointer[int(cellrow)][int(cellcol)]
                          cells[int(ID)].on_right_click(flagnum) #passes number of mines/flags remaining 
                          
                          #counts flagged cells
                          flagnum = 0
                          for cell in cells:
                              if cell.sprite == flaggedtile:
                                  flagnum += 1
                          #flags remaining
                          flagnum = minenum - flagnum
           
        if gamestart == True: #if game has started, pass time to counter, else pass 0
            seconds = (pygame.time.get_ticks()-start_ticks)/1000
            counter_digits(seconds)
        else:
            counter_digits(0)
        
        #set flags remaning digits
        mine_digits(int(flagnum))
        
        #reveals cells
        reveal(cells)
        
        no_flipped = 0 #finds number of flipped and draws cells
        for cell in cells:
            if cell.flipped == True:
                no_flipped += 1
            
            cell.set_sprite()
            cell.draw()
            
        if no_flipped == gamerows*gamecols - minenum: #determines win condition
            gamewin = True
            print("Cleared {:.0f} mines in {:.0f} seconds!".format(minenum, seconds))
            running = False
            break
         
        
            
            
        clock.tick(fps)
        pygame.display.update()
        
        
            
main()

pygame.quit()
