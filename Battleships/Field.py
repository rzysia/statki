'''
Created on 12 sty 2015

@author: Krzysztof
'''
import pygame
import unittest

class Field():
    
    def __init__(self, x, y):

        self.image = pygame.Surface([45, 45])
        self.image.set_alpha(75)
                
        self.x = x
        self.y = y
        self.content = None
        self.rectange = (x*45,y*45,(x+1)*45,(y+1)*45)

    def __str__(self):
        return "Field({0},{1})".format(self.x,self.y)

    def getId(self):
        return "{0}{1}".format(self.x,self.y)
    
    def getCoords(self, beginPoint):
        return (self.rectange[0] + beginPoint[0], self.rectange[1] + beginPoint[1])    
    

class TestField(unittest.TestCase):
    
    def testGetId(self):
        self.assertEqual(Field(1,1).getId(), "11")
    
    
if __name__ == '__main__':
    unittest.main()
    