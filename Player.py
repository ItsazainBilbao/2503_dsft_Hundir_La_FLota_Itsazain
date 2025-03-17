from Board import Board
import copy

class Player:

    #Constantes de los recursos del jugador
    CONST_RADAR_USES = 3
    usosRadar = 0
    CONST_TORPEDO_USES = 5
    torpedoCharged = False
    usosTorpedo = 0

    jugadorInfo = any
    #constructor
    def __init__(self, nombre = "", esHumano = False, tablero_Propio = None, tablero_Rival = None, rango = "Grumete"):
        self.nombre = nombre
        self.esHumano = esHumano
        self.rango = rango

        if(tablero_Propio is not None):
            self.tablero_propio = tablero_Propio
        else:
            self.tablero_propio = Board()

        if(tablero_Rival is not None):
            self.tablero_rival = tablero_Rival
        else:
            self.tablero_rival = Board()
    #depende de las victorias te asigan un rango
    def set_rango(self, num_partidas_ganadas):
        if(num_partidas_ganadas < 3):            
            rango = "Grumete"
        elif(num_partidas_ganadas < 20):
            rango = "Teniente"
        elif(num_partidas_ganadas < 50):
            rango = "Capitán"
        else:
            rango = "Almirante"
        self.rango = rango        
    #para asignar el nombre
    def set_name (self, name):
        self.nombre = name
    #para asignar el diccionario de datos
    def set_jugador_info(self, jugador):
        self.jugadorInfo = jugador        
        self.set_rango(jugador["partidas_ganadas"])

    #Método para inicializar las tablas dependiendo de como se quieran preparar    
    def setup_table(self, mode : str = "Random", size:int = 10):     
        self.tablero_propio.setupBoard(size, size)          
        self.tablero_propio.setupShips(mode)          
        pass
    #Se inicializa siempre con aguas, y se irá rellenando a medida que se va disparando
    def setup_rival_table(self, size:int = 10):
        self.tablero_rival.setupBoard(size, size)
        pass
    #se inicializa para el jugador
    def setup_jugador(self, mode : str = "Random", size:int = 10):
        self.usosTorpedo = 5
        self.setup_table(mode, size)
        self.setup_rival_table(size)
        pass
    pass
    #resetea el radar
    def resetRadar(self):
        self.usosRadar = self.CONST_RADAR_USES
    #va reduciendo en 1 los usos del radar
    def decreaseRadar(self):
        if(self.usosRadar > 0):
            self.usosRadar -= 1
        else:
            self.usosRadar = 0
    #resetea torpedos
    def resetTorpedo(self):
        self.usosTorpedo = self.CONST_TORPEDO_USES
    #reduce el uso de torpedos
    def decreaseTorpedo(self):
        if(self.usosTorpedo > 0):
            self.torpedoCharged = True
            self.usosTorpedo -= 1
        else:
            self.torpedoCharged = False
            self.usosTorpedo = 0
   

   