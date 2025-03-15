from Player import Player
from BattleMapUI import BattleMapUI
import random
import os
import Visuals

#Jugador 1
jugador_Humano = Player("Juan", True)
 #Jugador 2
jugador_Maquina = Player("Machine")

#Clase que se va a dedicar de la visualización por consola
battleMap = BattleMapUI()

#variables control flujo

Tocado = True #Variable que gestiona si el jugador activo ha tocado o no, en caso de tocar repite turno

clear = lambda: os.system('cls')

maxR = 9
isInGame = True
turnoJugador = True

def Setup():
    clear()
    print(Visuals.tituloText)
    print(Visuals.barcoText)


    #    Preparamos las tablas de cada jugador
    print("Bienvenido al simulador de Batalla Naval realista.")
    nombreI = input("Para iniciarte escribe tu nombre, grumete: ")
    jugador_Humano.set_name(nombreI)    
        
    pass

mode = { 1: "Manual", 2 : "Random", 3: "Static" }

def menu_partida_rapida():
    print("En estas simulaciones realistas podrás ponerte a prueba para ganar experiencia:\n\
Escoge una modalidad para desplegar tu flota de combate:\n\
          1.Manual (Escoge la posición inicial de tu flota. Sólo para almirantes de verdad)\n\
          2.Random (Escoge entre diferentes despliegues aleatorios y resuelve la situación)\n\
          3.Estático (Resuelve el conflicto con un tablero de inicio que será idéntico al del rival)\n\
          4.Atrás")
    opcion = input()    
    clear()
    if(opcion.isdigit()):
        if(0 < int(opcion) < 4):
            iniciar_Partida_Rapida(int(opcion))                    
    else:
        print("Opción inválida")


def iniciar_Partida_Rapida(nmodo):   
    nmodo = int(nmodo) 
    if( nmodo in mode.keys()):
        jugador_Humano.setup_jugador(mode[nmodo])        
        global maxR 
        maxR = jugador_Humano.tablero_propio.altura - 1
        jugador_Maquina.setup_jugador(mode[nmodo])
        jugador_Humano.resetRadar()
        global isInGame
        isInGame = True
        UpdateBattleMap()
        HandleGame()        
    else:
        print("Opción errónea")
    
    pass

       
def escoge_Modo_De_Juego():
    print("Escoge una opción (número): \n\
        1.Tutorial\n\
        2.Práctica Rápida\n\
        3.Perfil\n\
        4.Salir")
    opcion = input()
    clear()
    match opcion:
        case "1":
            ##Tutorial
            pass
        case "2":
            ##Partida Rápida
            menu_partida_rapida()            
            pass
        case "3":
            ##Perfil
            pass
        case "4":
            ##Salir
            return False            
        case _:
            print("Opción errónea, vuelve a introducir una opción válida: ")    
    return True
            


def getRandomValidCoord():    
    ranIte = True    
    
    while(ranIte):
        cord0 = random.randint(0, maxR)
        cord1 = random.randint(0, maxR)   
        
        if(jugador_Maquina.tablero_rival.get_Si_Tocado(cord0, cord1)):
            continue
        else:
            return cord0, cord1
    else:
        return cord0, cord1
        

def Action(esElTurnodelJugador : bool, touched : bool):       
    global isInGame       
    global turnoJugador
    while(touched and players_with_ships() and isInGame):        
        touched = False        
        if(esElTurnodelJugador):
            if(isInGame):
                cords = getCoordenades()                        
                touched = PerformAction(jugador_Humano, jugador_Maquina, cords)                
                turnoJugador = False                
            else:
                continue            
        else:            
            cords = getRandomValidCoord()
            touched = PerformAction(jugador_Maquina, jugador_Humano, cords)  
            turnoJugador = True      
    else:                       
        pass        
        

def UpdateBattleMap():      
    clear() 
    battleMap.imprimirTablero(jugador_Humano.tablero_propio, jugador_Humano.nombre)
    battleMap.imprimirTablero(jugador_Humano.tablero_rival, jugador_Maquina.nombre)

def PerformAction(jugadorAtacante : Player, jugadorDefensor : Player, coordenadas : int = (0,0)):  
    
    print(f"El jugador {jugadorAtacante.nombre} ha disparado a: {coordenadas}")    
    tocado = jugadorDefensor.tablero_propio.tocado(coordenadas[0], coordenadas[1])    
    ##Implementación Torpedo
    ##torpedoCharged = False
    if(tocado):                            
        print("TOCADO")
    else:
        print("AGUA")
    jugadorDefensor.tablero_propio.putMarca(coordenadas[0], coordenadas[1], tocado)  
    jugadorAtacante.tablero_rival.putMarca(coordenadas[0], coordenadas[1], tocado)

    UpdateBattleMap()
    return tocado

def players_with_ships():    
    return jugador_Maquina.tablero_propio.check_if_any_ship() and jugador_Humano.tablero_propio.check_if_any_ship()
 
def chars_and_nums(text):
    if not text:
        return [], []
    digits, chars = [], []
    for c in text:
        if c.isdigit():            
            digits.append(c)
        elif c.isalpha():
            chars.append(c)    
    if(len(digits) < 1):
            digits.append(1)    
        
    return int(''.join(map(str, digits))), str(''.join(chars))    

def coord0_inRange(coord : int):    
    if(coord < 0 or coord > maxR):
        return False
    else:
        return True
    
def activar_radar():
    if(jugador_Humano.usosRadar > 0):
        clear()
        battleMap.imprimirTablero(jugador_Maquina.tablero_propio, jugador_Maquina.nombre)
        battleMap.imprimirTablero(jugador_Humano.tablero_rival, jugador_Maquina.nombre)
        jugador_Humano.decreaseRadar()
        print("Usos de radar restantes: ", jugador_Humano.usosRadar)
    else:
        print("Ya no tienes usos de radar")

    pass


def check_if_comando(text):    
    match text.lower():
        case "ww":
            #print("Gana la partida")  
            jugador_Maquina.tablero_propio.remove_all_ships()   
            clear()            
            return True                
        case "r":
            #print("Radar")
            activar_radar()
            return True 
        case "t":
            #print("Cargar Torpedo")            
            jugador_Humano.decreaseTorpedo()
            return True
        case "q":
            global isInGame
            isInGame = False
            return True
            #Salir            
        case _:
            return False

def getCoordenades():
    isNotValidCor = True
    cor0 = 0
    cor1 = 0
    while (isNotValidCor and isInGame):
        cor = input("Introduce Coordenada válida (ej: 1A, 4b): ")

        if(check_if_comando(cor)):                                               
            continue

        spliced = chars_and_nums(cor) 
        cor0 = spliced[0] - 1                      

        if (len(spliced[1]) > 1 or len(spliced[1]) <= 0):
            print("Mala coordenada, te has pasado con las letras") 
            continue
        else:
            cor1 = (ord(spliced[1].upper()) - 65)
       
        if( not coord0_inRange(cor0) or not coord0_inRange(cor1)):
            print("Mala coordenada, no están en rango")
            pass
        elif(jugador_Humano.tablero_rival.get_Si_Tocado(cor0, cor1)):     
            print("Mala coordenada, ya le has dado")    
            continue
        else:            
            isNotValidCor = False
    else:                
        if(isInGame):
            return int(cor1), int(cor0)
        else:
            return 0,0
    
def whoWIn():
    if(jugador_Maquina.tablero_propio.check_if_any_ship() and jugador_Humano.tablero_propio.check_if_any_ship == False):
        return False
    elif(jugador_Maquina.tablero_propio.check_if_any_ship() == False and jugador_Humano.tablero_propio.check_if_any_ship):
        return True


def HandleGame():
    global isInGame
    global turnoJugador
    isInGame = True
    while(players_with_ships() and isInGame):   
        if(turnoJugador):      
            print("Turno de ", jugador_Humano.nombre)
            #Action(True, Tocado)
        else:
            print("Turno de ", jugador_Maquina.nombre)
            #Action(False, Tocado)
        Action(turnoJugador, True)
    else:
        ##Añadir quien gana
        if(isInGame != False):
            if(whoWIn):
                print(Visuals.winText)

            else:
                print(Visuals.loseText)   
        else:
            print("Saliste") 
        isInGame = False
    pass


def HandleUpdate():

    Setup()    

    enBucle = True

    while enBucle:
        enBucle = escoge_Modo_De_Juego()
      
    pass

#HandleUpdate()
    
