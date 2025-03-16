import json
import os

FILE_NAME = "players.json"

#Carga los jugadores desde el JSON, si no existe, crea un archivo vacío
def cargar_jugadores():    
    if not os.path.exists(FILE_NAME):  
        with open(FILE_NAME, "w") as f:
            json.dump({}, f)

    with open(FILE_NAME, "r") as f:
        return json.load(f)

#Guarda los jugadores en el json
def guardar_jugadores(jugadores):    
    with open(FILE_NAME, "w") as f:
        json.dump(jugadores, f, indent=4)

#Devuelve una entrada de jugador si existe, de lo contrario crea la entrada
def obtener_o_crear_jugador(nombre):    
    jugadores = cargar_jugadores()

    if nombre not in jugadores:
        print(f"Nuevo jugador {nombre} creado.")
        jugadores[nombre] = {
            "rango": "Grumete",
            "partidas_ganadas": 0,
            "partidas_perdidas": 0
        }
        guardar_jugadores(jugadores)

    return jugadores[nombre]

#Estas funciones son de conveniencia para pillar la info de cada entrada

def obtener_rango(nombre):    
    jugadores = cargar_jugadores()
    return jugadores.get(nombre, {}).get("rango", "Desconocido")

def obtener_partidas_ganadas(nombre):    
    jugadores = cargar_jugadores()
    return jugadores.get(nombre, {}).get("partidas_ganadas", 0)

def obtener_partidas_perdidas(nombre):    
    jugadores = cargar_jugadores()
    return jugadores.get(nombre, {}).get("partidas_perdidas", 0)

#Funciones para actualizar las entradas por conveniencia
def actualizar_rango(nombre, nuevo_rango):    
    jugadores = cargar_jugadores()
    if nombre in jugadores:
        jugadores[nombre]["rango"] = nuevo_rango
        guardar_jugadores(jugadores)
    else:
        print(f"Jugador {nombre} no encontrado.")

def actualizar_partidas(nombre, ganado=True):    
    jugadores = cargar_jugadores()
    
    if nombre in jugadores:
        if ganado:
            jugadores[nombre]["partidas_ganadas"] += 1
        else:
            jugadores[nombre]["partidas_perdidas"] += 1
        guardar_jugadores(jugadores)
    else:
        print(f"Jugador {nombre} no encontrado.")

