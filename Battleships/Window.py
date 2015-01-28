#!/usr/bin/python
'''
Created on 8 sty 2015

@author: Krzysztof
'''
import pygame
from pygame.locals import DOUBLEBUF,QUIT,KEYDOWN,K_ESCAPE
from sys import exit
from Board import Board
from Ship import Ship
from pygame.constants import K_SPACE

screen_size = (1215, 510)
playerBoardBeginPoint = (29, 31)
playerBoardEndPoint = (playerBoardBeginPoint[0] + 450, playerBoardBeginPoint[1] + 450)
aiBoardBeginPoint = (530, 31)
aiBoardEndPoint = (aiBoardBeginPoint[0] + 450, aiBoardBeginPoint[1] + 450)
singleRectWidth = 45
singleRectHeight = 45

class Battleships:
    
    def __init__(self):
        pygame.init()
        flag = DOUBLEBUF
        self.surface = pygame.display.set_mode(screen_size, flag)
        self.gamestate = 1    
        
        #do napisow
        self.headerFont = pygame.font.SysFont("Arial", 25, 1)    
        
        self.playerBoard = Board()
        self.aiBoard = Board()
        self.playersMovesBoard = Board()
        self.aiMovesBoard = Board()
        
        #do trzymania oznaczen na obu plansach - trafione i pudla
        #na liscie beda pudla
        self.shotsOnTarget = []
        self.missedShots = []
        
        #ladujemy obrazki
        self.background = pygame.image.load('img/background.png')
        self.explode = pygame.image.load('img/exp3.png')
#         self.ships = [Ship(1, 1040, 80), Ship(2, 1130, 70), Ship(3, 1040, 250), Ship(4, 1130, 230)]
        self.ships = []
        
        self.explodeFrames = [None] * 8
        self.explodeFrameRect = pygame.Rect(0,0,40,40)
        self.explodeActualFrame = -1
        self.explodeField = (None, None)
        
        for i in range(len(self.explodeFrames)):
            self.explodeFrameRect.left = i * 40
            self.explodeFrames[i] = self.explode.subsurface(self.explodeFrameRect)
                
        self.loop()
        
        
    def loop(self):
        listOfShips = [Ship(4),Ship(3),Ship(3),Ship(2),Ship(2),Ship(2),Ship(1),Ship(1),Ship(1),Ship(1), None]
        currentShip = listOfShips.pop(0)
        while self.gamestate == 1:
            
            pair = self.getFieldByMousePosition(pygame.mouse.get_pos())
                
            self.resetSurface()
            
            self.drawShips()
            
            if currentShip != None:
                self.surface.blit(self.headerFont.render('Trwa ustawianie statkow', True, (10,10,10)), (1030, 200))
                if self.drawShipUnderMouse(pygame.mouse.get_pos(), currentShip, pair) and len(listOfShips) > 0:
                    currentShip = listOfShips.pop(0)
            else:
                self.surface.blit(self.headerFont.render('Gra rozpoczeta', True, (10,10,10)), (1030, 200))               
                self.drawShots()            
                self.animateExplode()
            
            
            
            if pair != None:
                field = pair[0]
                if field != None:
                    self.surface.blit(field.image, field.getCoords(pair[1]))
                
            self.handleEvents(pair)
            
                
            
            pygame.display.flip()
            
        self.gameExit()
  
    
    def getFieldByMousePosition(self, position):
        if position[0] < playerBoardEndPoint[0]:
            return self.getFiledFromPlayerBoard(position)
        return self.getFieldFromAiBoard(position)
                        
        
    
    def getFiledFromPlayerBoard(self, position):
        if position[0] < playerBoardBeginPoint[0] or position[0] > playerBoardEndPoint[0] or position[1] < playerBoardBeginPoint[1] or position[1] > playerBoardEndPoint[1]:
            return None        
        xIndex = (position[0] - playerBoardBeginPoint[0]) / singleRectWidth
        yIndex = (position[1] - playerBoardBeginPoint[1]) / singleRectHeight        
        mouseOnId = "{0}{1}".format(xIndex, yIndex)
        
        return (self.playerBoard.getFieldById(mouseOnId), playerBoardBeginPoint)
    
    def getFieldFromAiBoard(self, position):
        if position[0] < aiBoardBeginPoint[0] or position[0] > aiBoardEndPoint[0] or position[1] < aiBoardBeginPoint[1] or position[1] > aiBoardEndPoint[1]:
            return None        
        xIndex = (position[0] - aiBoardBeginPoint[0]) / singleRectWidth
        yIndex = (position[1] - aiBoardBeginPoint[1]) / singleRectHeight        
        mouseOnId = "{0}{1}".format(xIndex, yIndex)
        
        return (self.aiBoard.getFieldById(mouseOnId), aiBoardBeginPoint)
    
    def resetSurface(self):
        self.surface.fill((220, 220, 220))
        self.surface.blit(self.headerFont.render('Gra w statki', True, (10,10,10)), (1030, 10))
        self.surface.blit(self.background, (0, 0))
        
    def handleEvents(self, pair):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.gamestate = 0
            if event.type == pygame.MOUSEBUTTONDOWN and pair != None:
                if pair[0].content == None:                  
                    if not self.checkIfPresentOnList(self.missedShots, pair[0]):                    
                        self.missedShots.append(pair)
                else:
                    if not self.checkIfPresentOnList(self.shotsOnTarget, pair[0]):
                        self.explodeActualFrame = 0
                        self.explodeField = pair
                        self.shotsOnTarget.append(pair)
                
                    
                
    def checkIfPresentOnList(self, listToCheck, element):
        for pair in listToCheck:
                if pair[0] == element:
                    return True
        return False           
                
    def drawShots(self):
        self.drawMissed()
        self.drawHited()

    def drawMissed(self):
        for pair in self.missedShots:
            coords = [x + 22 for x in pair[0].getCoords(pair[1])]
            pygame.draw.circle(self.surface, (0,0,0), coords, 5)
    
    def drawHited(self):
        for pair in self.shotsOnTarget:
            coordsBSstart = pair[0].getCoords(pair[1]) 
            coordsBSend = [x + 45 for x in pair[0].getCoords(pair[1])]
            
            pygame.draw.line(self.surface, (255,0,0), coordsBSstart, coordsBSend, 5)
            pygame.draw.line(self.surface, (255,0,0), (coordsBSstart[0],coordsBSend[1]), (coordsBSend[0],coordsBSstart[1]), 5)
            
    
    def drawShips(self):
        for ship in self.ships:
            self.surface.blit(ship.image, ship.coords)
            
               
    def drawShipUnderMouse(self, coords, ship, pair):
        coords = (coords[0]-20, coords[1])
        self.surface.blit(ship.image, coords)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.gamestate = 0
            if event.type == pygame.MOUSEBUTTONDOWN and pair[1][0] < playerBoardEndPoint[0]:
                if self.setContent(pair,ship):
                    ship.setCoords(pair[0].getCoords(pair[1]))
                    self.ships.append(ship)
                    return True
            if event.type == KEYDOWN and event.key == K_SPACE:
                ship.changeOrientation()
        return False
    
    
    def setContent(self, pair, ship):
        lenght = ship.getLenght()
        startFieldId = pair[0].getId()
        fields = [pair[0]]
        
        for _ in range(lenght-1):
            if ship.orientation == 1:
                startFieldId = "{0}{1}".format(startFieldId[0], int(startFieldId[1]) + 1)
            else:
                startFieldId = "{0}{1}".format(int(startFieldId[0]) + 1, startFieldId[1])
            field = self.playerBoard.getFieldById(startFieldId)
            if field != None:
                fields.append(field)
            else:           #tym zabezpieczamy sie przed statkiem nie mieszczacym sie na planszy
                return False
        
        for f in fields:
            if not self.playerBoard.checkField(f.getId()):
                return False
        
        for f in fields:
            f.content = "anything"            
            
        return True
    
       
    def animateExplode(self):
        if self.explodeActualFrame >= 0 and self.explodeActualFrame < 21:
            self.explodeActualFrame += 1
            coordsForExplode = [x + 4 for x in self.explodeField[0].getCoords(self.explodeField[1])]
            
            self.surface.blit(self.explodeFrames[self.explodeActualFrame/3], coordsForExplode)
        
    def gameExit(self):
        pygame.quit()
        exit()
            
if __name__ == '__main__':
    Battleships()
