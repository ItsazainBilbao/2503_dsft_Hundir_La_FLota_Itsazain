from Board import Board
import copy

class Player:


    CONST_RADAR_USES = 3
    usosRadar = 0
    CONST_TORPEDO_USES = 5
    torpedoCharged = True
    usosTorpedo = 0

    def __init__(self, nombre = "", esHumano = False, tablero_Propio = None, tablero_Rival = None):
        self.nombre = nombre
        self.esHumano = esHumano

        if(tablero_Propio is not None):
            self.tablero_propio = tablero_Propio
        else:
            self.tablero_propio = Board()

        if(tablero_Rival is not None):
            self.tablero_rival = tablero_Rival
        else:
            self.tablero_rival = Board()

        

    def set_name (self, name):
        self.nombre = name

    #Método para inicializar las tablas dependiendo de como se quieran preparar    
    def setup_table(self, mode : str = "Random", size:int = 10):     
        self.tablero_propio.setupBoard(size, size)          
        self.tablero_propio.setupShips(mode)          
        pass
    #Se inicializa siempre con aguas, y se irá rellenando a medida que se va disparando
    def setup_rival_table(self, size:int = 10):
        self.tablero_rival.setupBoard(size, size)
        pass
    def setup_jugador(self, mode : str = "Random", size:int = 10):
        self.setup_table(mode, size)
        self.setup_rival_table(size)
        pass
    pass

    def resetRadar(self):
        self.usosRadar = self.CONST_RADAR_USES

    def decreaseRadar(self):
        if(self.usosRadar > 0):
            self.usosRadar -= 1
        else:
            self.usosRadar = 0

    def resetTorpedo(self):
        self.usosTorpedo = self.CONST_TORPEDO_USES

    def decreaseTorpedo(self):
        if(self.usosTorpedo > 0):
            self.torpedoCharged = True
            self.usosTorpedo -= 1
        else:
            self.torpedoCharged = False
            self.usosTorpedo = 0
   

   