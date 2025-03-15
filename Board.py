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

    barcos_por_size = {4: 1, 3: 1, 2: 2, 1: 3}

    coordVisitadas = set()

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
            if(self.check_if_any_ship_in(crd0, crd1) or not self.check_adjacent_empty(crd0, crd1)):
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
            #Esto lo he movido al game manager, porque no conseguía hacer que enseñase el tablero          
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
            if isVertical:
                if not self.check_adjacent_empty(crd0 + i, crd1): 
                    return True
            else:
                if not self.check_adjacent_empty(crd0, crd1 + i):  
                    return True
        return False

    def remove_all_ships(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] == self.CONST_SHIP:
                    self.tablero[i][j] = self.CONST_WATER

    def destroy_all_ships(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] == self.CONST_SHIP:
                    self.tablero[i][j] = self.CONST_IMPACTED_SHIP
        
    def check_adjacent_empty(self, crd0, crd1):    
        #todas las direcciones de alrededor de una casilla
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]    
    
        for dx, dy in directions:
            adjX = crd0 + dx
            adjY = crd1 + dy
        
            if 0 <= adjX < self.altura and 0 <= adjY < self.base:
                if self.tablero[adjX][adjY] == self.CONST_SHIP:
                    return False #Si hay barco false
        return True 

    
    def setupShipManually(self, size: int, cord: tuple, direction: str):
        
        x, y = cord        
        
        if self.canPlaceShip(x, y, size, direction):
            
            for i in range(size):
                match direction:
                    case "N":
                        self.putShip(x - i, y)
                    case "S":
                        self.putShip(x + i, y)
                    case "E":
                        self.putShip(x, y + i)
                    case "O":
                        self.putShip(x, y - i)
                    case _:                        
                        pass
                #Llamada para imprimir?

        else:
            print(f"No se puede colocar el barco en {cord} en dirección {direction}.")
        
    def canPlaceShip(self, x: int, y: int, size: int, direction: str):        
        #Miramos si el barco puede entrar en las coordenadas con la dirección
        match direction:
            case "N":
                if x - size < 0:  
                    return False
                for i in range(size):
                    if self.check_if_any_ship_in(x - i, y): 
                        return False
                pass
            case "S":
                if x + size > self.altura:  
                    return False
                for i in range(size):
                    if self.check_if_any_ship_in(x + i, y):  
                        return False
                pass
            case "E":
                if y + size > self.base: 
                    return False
                for i in range(size):
                    if self.check_if_any_ship_in(x, y + i):  
                        return False
                pass
            case "O":
                if y - size < 0:  
                    return False
                for i in range(size):
                    if self.check_if_any_ship_in(x, y - i):  
                        return False
                pass
            case _:
                pass

        return True
    
    def verificar_hundido(self, x, y):       
        #Si la coordenada está en la lista no hace falta volver a revisarla
        #Sin embargo tiene bug con la de 4 y si hundimos el barco desde el centro hacia las esquinas
        #una de las esquinas no las cuenta
        if (x, y) in self.coordVisitadas:
            return True 

        #Añade la casilla a la lista
        self.coordVisitadas.add((x, y))

        #lista de las direcciones n,s,o,e
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.altura and 0 <= ny < self.base:
                if self.tablero[nx][ny] == self.CONST_SHIP:  #si se encuentra un barco no está hundido
                    return False
                elif self.tablero[nx][ny] == self.CONST_IMPACTED_SHIP:  
                    #Si encontramosun impacto de barco se Verificamos recursivamente alrededor del impacto en una direccion
                    return self.check_direction(nx, ny, dx, dy)
        
        #Si todas las casillas son agua o impacto agua se la suda y te devuelve true
        return True

    def check_direction(self, x, y, dx, dy):        
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.altura and 0 <= ny < self.base:
            if self.tablero[nx][ny] == self.CONST_SHIP:  #Si encontramos barco quiere decir que no se ha hundido
                return False
            elif self.tablero[nx][ny] == self.CONST_IMPACTED_SHIP:  #si encuentra un barco impactado comprueba los siguientes
                return self.verificar_hundido(nx, ny)  #Llamada recursiva
    
        return True  #Si no se encontró un barco ni impactos devuelve true

    