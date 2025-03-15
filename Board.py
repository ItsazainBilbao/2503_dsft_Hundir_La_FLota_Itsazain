import numpy
import copy
import random
class Board:

    CONST_WATER = "0"
    CONST_SHIP = "1"
    CONST_IMPACTED_SHIP = "x"
    CONST_IMPACTED_WATER = "o"

    CONST_altura = 10
    CONST_base = 10

    #tablero = tablero = numpy.zeros((10, 10), dtype=str)    

    def __init__(self, altura : int = 10, base : int = 10, tablero = None):      
        if tablero is not None:
            self.tablero = tablero
        else:
            self.tablero = []
        
        if(4 < altura < 25 or 4 < base < 25):
            self.altura = altura
            self.base = base
        else:
            self.altura = self.CONST_altura
            self.base = self.CONST_base

        pass    
            
    def setupBoard(self, altura= 10, base = 10):
        self.altura = altura
        self.base = base
        self.tablero = copy.deepcopy(numpy.zeros((self.altura, self.base), dtype=str)).copy()
        self.tablero.fill(self.CONST_WATER)    


    def getRandomValidCoordInRange(self, xMax, yMax):    
        ranIte = True
        
        while(ranIte):
            crd0 = random.randint(0, xMax)            
            crd1 = random.randint(0, yMax)              
            if(self.check_if_any_ship_in(crd0, crd1)):
                continue
            else:
                return crd0, crd1   
        else:
            
            return crd0, crd1


    def setupShip(self, size : int, isVertical : bool):
        cord = (0,0)
        
        if(isVertical):
            cord = self.getRandomValidCoordInRange(self.altura - size -1, self.base - 1)            
        else:
            cord = self.getRandomValidCoordInRange(self.altura -1 , self.base - size - 1)        
        if(not self.ship_of_Size_in(cord[0],cord[1], size, isVertical)):
            for i in range(0, size):
                if isVertical:
                    self.putShip(cord[0] + i, cord[1])
                else:
                    self.putShip(cord[0], cord[1] + i)
        
  
    def putShip(self, cord0, cord1):
        self.tablero[cord0][cord1] = self.CONST_SHIP
        pass

    def setupSpecificSetofShipRandomly(self, shipSize, times):
        inVertical = bool(random.randint(0, 1))
        for i in range(times):
            self.setupShip(shipSize, inVertical)
        pass

    def setupShipRandomly(self, timesSize4: int = 1, timesSize3:int =2, timesSize2:int=3, timeSize1:int =4):
        self.setupSpecificSetofShipRandomly(4, timesSize4)
        self.setupSpecificSetofShipRandomly(3, timesSize3)
        self.setupSpecificSetofShipRandomly(2, timesSize2)
        self.setupSpecificSetofShipRandomly(1, timeSize1)

        pass


    def setupShips(self, mode : str):              
        if(mode == "Manual"):
            
            pass
        elif(mode == "Random"):
            self.setupShipRandomly()            
            pass
        elif (mode == "Static"):             #   1   2   3   4   5   6   7   8   9  10
            self.tablero = [["0","0","0","0","0","0","0","0","0","0"], #A
                            ["0","1","1","0","0","0","1","0","0","0"], #B
                            ["0","0","1","1","0","0","1","0","0","0"], #C
                            ["0","0","0","0","0","0","1","1","0","0"], #D
                            ["1","1","1","0","0","0","0","1","0","0"], #F
                            ["0","0","0","0","0","0","0","0","0","0"], #G
                            ["0","1","0","0","0","0","0","1","0","0"], #H
                            ["0","1","0","0","0","1","0","0","1","0"], #I
                            ["0","1","0","0","0","0","1","0","0","0"], #J
                            ["0","1","0","0","0","0","0","0","0","0"],]#K                       
            pass   
        else:
             print("Error al escoger modo")    
        

    def tocado(self, posX, posY):        
        casilla = copy.deepcopy(self.tablero[posX][posY])
        tocado = True
        if(casilla == self.CONST_WATER):  
            tocado = False            
        elif(casilla == self.CONST_SHIP):
            tocado = True                         
        return tocado       
    
    def putMarca(self, posX, posY, tocado):
        if(tocado):
            res = self.CONST_IMPACTED_SHIP 
        else:
            res = self.CONST_IMPACTED_WATER            
        self.tablero[posX][posY] = res                
    
    def get_Si_Tocado(self, posX, posY):      
        
        if(self.tablero[posY][posX] == self.CONST_IMPACTED_SHIP or self.tablero[posY][posX] == self.CONST_IMPACTED_WATER):
            return True
        else:
            return False
        
    def check_if_any_ship(self):        
        for fila in self.tablero:
            for casilla in fila:      
                if(casilla == self.CONST_SHIP):                    
                    return True
        return False   

    def check_if_any_ship_in(self, crd0 : int, crd1 : int):            
        if(self.tablero[crd0][crd1] == self.CONST_SHIP):            
            return True
        else:
            return False
            
    def ship_of_Size_in(self, crd0 : int, crd1 : int, size :int, isVertical : bool):    
           
        for i in range(size):
            if(isVertical):                
                return self.check_if_any_ship_in(crd0 + i, crd1)
            else:                
                return self.check_if_any_ship_in(crd0, crd1 + i)

    def remove_all_ships(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] == self.CONST_SHIP:
                    self.tablero[i][j] = self.CONST_WATER
        

   

    