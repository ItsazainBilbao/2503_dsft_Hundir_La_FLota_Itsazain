from Player import Player
from BattleMapUI import BattleMapUI
import random
import os
import Visuals
from playsound import playsound
from SaveManager import *

#Jugador 1
jugador_Humano = Player("Juan", True)
 #Jugador 2
jugador_Maquina = Player("Machine")

#Clase que se va a dedicar de la visualización por consola
battleMap = BattleMapUI()

#variables control flujo

Tocado = True #Variable que gestiona si el jugador activo ha tocado o no, en caso de tocar repite turno

clear = lambda: os.system('cls') #Sirve para borrar la pantalla

#Variables globales para controlar flujo y cosas
maxR = 9 #Este para llevar los limites del tablero
isInGame = True #Para saber si se está en juego, si es false se salta checks y va hacia el menu principal sin dar victoria
turnoJugador = True #Para saber si es el turno del jugador

#Función para pedir el nombre del jugador y cargar o crear su entrada en el Json que gestiona los perfiles
def Setup():
    clear()
    print(Visuals.tituloText)
    print(Visuals.barcoText)
    #    Preparamos las tablas de cada jugador
    print("Bienvenido al simulador de Batalla Naval realista.")
    nombreI = input("Para iniciarte escribe tu nombre, grumete: ")
    jugador_Humano.set_name(nombreI)     
    jugador = obtener_o_crear_jugador(nombreI)   
    jugador_Humano.set_jugador_info(jugador)               

#Función para mostrar el perfil del jugador activo
def mostrar_perfil():
    jugador = obtener_o_crear_jugador(jugador_Humano.nombre)
    nom = jugador_Humano.nombre     
    jugador_Humano.set_jugador_info(jugador)  
    print(Visuals.tituloText)
    print(Visuals.barcoText)
    print("Nombre: ", nom)    
    jugador_Humano.set_rango(obtener_partidas_ganadas(nom))
    actualizar_rango(nom, jugador_Humano.rango)
    print("Rango: ", obtener_rango(nom))
    print("Simulaciones Éxitosas: ", obtener_partidas_ganadas(nom))
    print("Simulaciones 'Accidentadas': ", obtener_partidas_perdidas(nom))    
    while(True):
        salirI = input("Escribe s para salir: ")
        if(salirI.lower() =="s"):
            break
        else:
            clear()
            mostrar_perfil()

    pass

#Diccionario para llevar el control más cómodo de los diferentes modos en el modo rápido
mode = { 1: "Manual", 2 : "Random", 3: "Static", 5:"Tuto" }

#Función que gestiona el menu de partida rápida
def menu_partida_rapida():
    clear()
    print(Visuals.tituloText)
    print(Visuals.barcoText)
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


#Función que convierte unas coordenadas metidas como letra y número en dos números para los índices
#EN otra función esto está hecho a mano, y esto lo uso para reutilizarlo al meter los barcos a mano
def coords_to_index(coord: str):       
        digits, chars = chars_and_nums(coord)
        x = digits - 1
        y = ord(chars.upper()) - 65
        return x, y

#Inicia todas las variables y tablas con el tamaño adecuado al modo para la partida rápida
def iniciar_Partida_Rapida(nmodo):   
    nmodo = int(nmodo) 
    if( nmodo in mode.keys()):
        if(nmodo != 1):
            jugador_Humano.setup_jugador(mode[nmodo])        
        else:
            jugador_Humano.tablero_propio.setupBoard()
            setup_manual()
            pass        
        global maxR         
        maxR = jugador_Humano.tablero_propio.altura - 1
        global turnoJugador
        turnoJugador = True
        jugador_Maquina.setup_jugador()
        jugador_Humano.resetRadar()
        global isInGame
        isInGame = True
        UpdateBattleMap()
        HandleGame()        
    else:
        print("Opción errónea")
    
    pass

#Función para meter los barcos de forma manual.
#Quise hacerlo en Board, pero no podia imprimir bien después de cada entrada
def setup_manual():
        barcos_por_size = jugador_Humano.tablero_propio.barcos_por_size

        for size, cantidad in barcos_por_size.items():
            for _ in range(cantidad):
                valid_input = False
                while not valid_input:
                    coord_input = input(f"Introduce la coordenada inicial para el barco de tamaño {size} (ej: 4A): ")
                    direction_input = input("Introduce la dirección (N, S, E, O): ").upper()

                    x, y = coords_to_index(coord_input)                    
                    if jugador_Humano.tablero_propio.canPlaceShip(x, y, size, direction_input):
                        jugador_Humano.tablero_propio.setupShipManually(size, (y, x), direction_input)
                        valid_input = True
                        clear()                        
                        print(jugador_Humano.tablero_propio.tablero)
                        battleMap.imprimirTablero(jugador_Humano.tablero_propio, jugador_Humano.nombre)
                    else:
                        print(f"Posición o dirección inválida para el barco de tamaño {size}. Inténtalo de nuevo.")

#El menu principal para escoger el modo.
def escoge_Modo_De_Juego():
    clear()
    print(Visuals.tituloText)
    print(Visuals.barcoText)
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
            clear()            
            menu_tutorial()
            pass
        case "2":
            ##Partida Rápida
            menu_partida_rapida()            
            pass
        case "3":
            ##Perfil
            mostrar_perfil()
            pass
        case "4":
            ##Salir
            return False            
        case _:
            print("Opción errónea, vuelve a introducir una opción válida: ")    
    return True
            
#Función para pillar una coordenada válida aleatoria para la máquina
def getRandomValidCoord():    
    ranIte = True    
    
    while(ranIte):
        cord0 = random.randint(0, maxR)
        cord1 = random.randint(0, maxR)   
        
        if(jugador_Maquina.tablero_rival.get_Si_Tocado(cord0, cord1)): #Si ya ha golpeado en esa posición, busca otra
            continue
        else:
            return cord0, cord1
    else:
        return cord0, cord1
        
#Función que lleva la acción de cada jugador. Si alguien ha golpeado un barco, se repite. Si no, pasa al otro jugador
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
        
#Función de conveniencia para imprimir las tablas bonitas
def UpdateBattleMap():      
    clear() 
    battleMap.imprimirTablero(jugador_Humano.tablero_propio, jugador_Humano.nombre)
    battleMap.imprimirTablero(jugador_Humano.tablero_rival, jugador_Maquina.nombre)

#Función que lleva a cabo el disparo y toda su lógica
def PerformAction(jugadorAtacante : Player, jugadorDefensor : Player, coordenadas : int = (0,0)):  
    
    print(f"El jugador {jugadorAtacante.nombre} ha disparado a: {coordenadas}")    
    tocado = jugadorDefensor.tablero_propio.tocado(coordenadas[0], coordenadas[1])    
    playsound("./sonido/explosion-91872.mp3")
    jugadorDefensor.tablero_propio.putMarca(coordenadas[0], coordenadas[1], tocado)  
    jugadorAtacante.tablero_rival.putMarca(coordenadas[0], coordenadas[1], tocado)
    UpdateBattleMap()
    if(tocado):                            
        print("TOCADO")
        if(jugadorAtacante.torpedoCharged):
            jugadorDefensor.tablero_propio.destroy_all_ships()
            jugadorAtacante.torpedoCharged = False
        if(jugadorDefensor.tablero_propio.verificar_hundido(coordenadas[0], coordenadas[1])):
            print("Hundido")
            playsound("./sonido/apique.mp3")
    else:
        print("AGUA")
        playsound("./sonido/splash-effect-229315.mp3")    

    UpdateBattleMap()
    return tocado

#función que devuelve si quedan barcos en algún tablero. Para romper el juego y saber si se termina o no
def players_with_ships():    
    return jugador_Maquina.tablero_propio.check_if_any_ship() and jugador_Humano.tablero_propio.check_if_any_ship()
 
#Función que le metes un texto y te separa los caracteres y numeros
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

#Me acabo de dar cuenta de que ya tengo esta función arriba, pero si la quito el juego me peta. No tocar
def coords_to_index(coord: str):    
    digits, chars = chars_and_nums(coord)
    x = digits - 1
    y = ord(chars.upper()) - 65
    return x, y
#Mira si la coordenada está dentro del rango del tablero
def coord0_inRange(coord : int):    
    if(coord < 0 or coord > maxR):
        return False
    else:
        return True
#Función que activa el radar, básicamente imprime otra vez los tableros enseñando los barcos del rival
def activar_radar():
    if(jugador_Humano.usosRadar > 0):
        clear()
        battleMap.imprimirTablero(jugador_Humano.tablero_propio, jugador_Humano.nombre)
        battleMap.imprimirTablero(jugador_Maquina.tablero_propio, jugador_Maquina.nombre, True)        
        jugador_Humano.decreaseRadar()
        print("Usos de radar restantes: ", jugador_Humano.usosRadar)
    else:
        print("Ya no tienes usos de radar")

    pass

#Función que mira si se ha metido un comando en vez de una coordenada
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
            playsound("./sonido/sonar-sweep-beep-80957.mp3")
            return True 
        case "t":
            #print("Cargar Torpedo")   
            jugador_Humano.decreaseTorpedo()
            print("Usos Torpedo", jugador_Humano.usosTorpedo, jugador_Humano.torpedoCharged)
            return True
        case "q":
            global isInGame
            isInGame = False            
            return True
            #Salir            
        case _:
            return False

#Básicamente la función que el pide al jugador las coordenadas y luego las devuelve validadas para la lógica
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
    
#FUnción conveniente para saber quien gana o pierde y así luego enseñar el mensaje correcto y sumar donde se debe
def whoWIn():
    if(jugador_Maquina.tablero_propio.check_if_any_ship() and jugador_Humano.tablero_propio.check_if_any_ship == False):
        return False
    elif(jugador_Maquina.tablero_propio.check_if_any_ship() == False and jugador_Humano.tablero_propio.check_if_any_ship):
        return True

#Función que lleva toda la lógica de la partida
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
            clear()
            if(whoWIn):                               
                print(Visuals.winText)     
                actualizar_partidas(jugador_Humano.nombre, ganado=True)                    
                bucleEspera()
            else:                
                print(Visuals.loseText)   
                actualizar_partidas(jugador_Humano.nombre, ganado=False)
                bucleEspera()                
        else:
            print("Saliste") 
            clear()
        isInGame = False
    pass

#Función que espera a que alguien pulse una tecla o así, para que se vea el mensaje final y probar yo algunos prints a lo debug
def bucleEspera():
    while(True):
        inpu = input()
        if(inpu != None):
            break

#La función donde está todo el juego corriendo hasta que alguien rompe el bucle
def HandleUpdate():

    Setup()    

    enBucle = True

    while enBucle:
        enBucle = escoge_Modo_De_Juego()
      
    pass
   
####TUtorial

#Aquí creo las diferentes funciones de tutorial. Podría haberlo hecho más bonito y reutilziar más código
#Pero es que ya estaba muy cansado

def inicial_tutorial_1():
    jugador_Humano.setup_jugador("Tuto", 5) 
    global maxR         
    maxR = jugador_Humano.tablero_propio.altura - 1
    global turnoJugador
    turnoJugador = True
    jugador_Maquina.setup_jugador("Tuto", 5)
    jugador_Humano.resetRadar()
    global isInGame
    isInGame = True
    UpdateBattleMap()
    HandleGame()      
    pass

def inicial_tutorial_2():
    jugador_Humano.setup_jugador("Tuto2", 5) 
    global maxR         
    maxR = jugador_Humano.tablero_propio.altura - 1
    global turnoJugador
    turnoJugador = True
    jugador_Maquina.setup_jugador("Tuto2", 5)
    jugador_Humano.resetRadar()
    global isInGame
    isInGame = True
    UpdateBattleMap()
    HandleGame() 
    pass

def inicial_tutorial_3():
    jugador_Humano.setup_jugador("Tuto3", 5) 
    global maxR         
    maxR = jugador_Humano.tablero_propio.altura - 1
    global turnoJugador
    turnoJugador = True
    jugador_Maquina.setup_jugador("Tuto3", 5)
    jugador_Humano.resetRadar()
    global isInGame
    isInGame = True
    UpdateBattleMap()
    HandleGame() 
    pass
    pass

#La función que gestiona el menu del tutorial
def menu_tutorial():    
    print(Visuals.tituloText)
    print(Visuals.barcoText)
    print("Escoge nivel de Tutorial: \n"
    "   1.Disparar\n"
    "   2.Sonar\n"
    "   3.Torpedo\n"
    "   4.Salir\n")
    inpu = input("Inserta opción: ")

    match inpu:
        case "1":
            inicial_tutorial_1()
            pass
        case "2":
            inicial_tutorial_2()
            pass
        case "3":
            inicial_tutorial_3()
            pass
        case _:
            pass

    pass