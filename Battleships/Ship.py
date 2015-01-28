'''
Created on 19 sty 2015

@author: Krzysztof
'''
import pygame

class Ship:
     
    def __init__(self, howLong, x=0, y=0):
        self.image = pygame.image.load(self.getImageName(howLong))
        self.lenght = howLong
        self.coords = (x,y)
        self.orientation = 1    #1 to pionowo, 0 to poziomo
        
    def getImageName(self, howLong):
        if howLong == 1:
            return "img/b1.png"
        if howLong == 2:
            return "img/b2.png"
        if howLong == 3:
            return "img/b3.png"
        if howLong == 4:
            return "img/b4.png"
        
        
    def setCoords(self, x):
        self.coords = x
        
    def getLenght(self):
        return self.lenght
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientationVertical(self):
        self.orientation = 1
        
    def setOrientationHorizontal(self):
        self.orientation = 0
        
    def changeOrientation(self):
        if self.orientation == 1:
            self.setOrientationHorizontal()
            self.image = pygame.transform.rotate(self.image, 90)
        else:
            self.setOrientationVertical()
            self.image = pygame.transform.rotate(self.image, 270)
        
        
        
    