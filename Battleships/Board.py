#!/usr/bin/python
'''
Created on 12 sty 2015
@author: Krzysztof
'''
import unittest
from Field import Field

class Board:
    
    def __init__(self,maxIndex=10):
        self.fields = []
        
        for i in range(maxIndex):
            new = []
            for j in range(maxIndex):
                new.append(Field(i,j))
                
            self.fields.append(new)

            
    
    def getFieldById(self, fieldId):
#         fieldToReturn = None
        for fieldList in self.fields:
            for field in fieldList:
                if field.getId() == fieldId:
                    return field
        return None     
    
    def checkField(self, fieldId):
        field = self.getFieldById(fieldId)
        if not field.content == None:
            return False
        return self.checkNeighbors(fieldId)
    
    def checkNeighbors(self, fieldId):
        posX,posY = int(fieldId[0]),int(fieldId[1])
        if posX > 0:
            if not self.getFieldById("{0}{1}".format(posX-1,posY)).content == None:
                return False            
        if posX < 9:
            if not self.getFieldById("{0}{1}".format(posX+1,posY)).content == None:
                return False            
        if posY > 0:
            if not self.getFieldById("{0}{1}".format(posX,posY-1)).content == None:
                return False            
        if posY < 9:
            if not self.getFieldById("{0}{1}".format(posX,posY+1)).content == None:
                return False
            
        if posY < 9 and posX < 9:
            if not self.getFieldById("{0}{1}".format(posX+1,posY+1)).content == None:
                return False    
        if posY > 0 and posX > 0:
            if not self.getFieldById("{0}{1}".format(posX-1,posY-1)).content == None:
                return False
        if posY > 0 and posX < 9:
            if not self.getFieldById("{0}{1}".format(posX+1,posY-1)).content == None:
                return False
        if posY < 9 and posX > 0:
            if not self.getFieldById("{0}{1}".format(posX-1,posY+1)).content == None:
                return False
            
        
        return True        
                

class TestBoard(unittest.TestCase):
    
    def testGetFieldById(self):
        board = Board(1)
        field = board.getFieldById("00")
        self.assertFalse(field == None)      
        self.assertEqual(field.getId(), "00")    
    
if __name__ == '__main__':
    unittest.main()
    