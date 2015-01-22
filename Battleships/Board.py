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
                
                

class TestBoard(unittest.TestCase):
    
    def testGetFieldById(self):
        board = Board(1)
        field = board.getFieldById("00")
        self.assertFalse(field == None)      
        self.assertEqual(field.getId(), "00")    
    
if __name__ == '__main__':
    unittest.main()
    