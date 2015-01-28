'''
Created on 22 sty 2015

@author: Krzysztof
'''
from Board import Board
import Ship
import random


class AI:
    
    def __init__(self, board):
        self.board = board
        self.fillBoard(board)
        
    def fillBoard(self, board):
        listOfShips = [Ship(4),Ship(3),Ship(3),Ship(2),Ship(2),Ship(2),Ship(1),Ship(1),Ship(1),Ship(1), None]
        currentShip = listOfShips.pop(0)
        while not currentShip == None:
            self.putShip(board, currentShip)
            currentShip = listOfShips.pop(0)
            
    def putShip(self, board, ship):    
        if random.randint(1,10)%2 == 1:
            ship.changeOrientation()
        field = self.getRandomField()
        while not self.setContent(field, ship):
            field = self.getRandomField()
            
    def setContent(self, field, ship):
        lenght = ship.getLenght()
        startFieldId = field.getId()
        fields = [field]
        
        for _ in range(lenght-1):
            if ship.orientation == 1:
                startFieldId = "{0}{1}".format(startFieldId[0], int(startFieldId[1]) + 1)
            else:
                startFieldId = "{0}{1}".format(int(startFieldId[0]) + 1, startFieldId[1])
            fieldTemp = self.board.getFieldById(startFieldId)
            if fieldTemp != None:
                fields.append(fieldTemp)
            else:           #tym zabezpieczamy sie przed statkiem nie mieszczacym sie na planszy
                return False
        
        for f in fields:
            if not self.board.checkField(f.getId()):
                return False
        
        for f in fields:
            f.content = "anything"            
            
        return True  
    
    def getRandomField(self):
        pass        