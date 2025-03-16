# 🚢 SImulación de Batalla Naval realista 🚢

## Descripción
Proyecto de hundir la flota en pyhton con un menu y diferentes modos de juego. La capacidad de guardar y cargar perfiles.
## Estructura
### main.py
Fichero en el que se llama a la lógica del juego
### GameManager.py
Fichero donde se gestiona toda la lógica del juego. Importa Player.py y BattleUI.py para gestionarlo todo.
### Player.py
CLase Jugador que importa y utiliza Board.py y su clase para guardar las tablas y demás datos.  
Cada jugador tiene dos tablas, una para sus barcos y otra para marcar donde el rival tiene sus barcos y aguas.
### Board.py
Clase donde se encuentra toda la lógica y gestión de una tabla del juego. Tanto la creación de la misma, como la inicialización de los barcos y demás.
### BattleMapUI.py
Clase que dibuja de forma bonita las tablas de juego empleando la librería de RICH
### SaveManager.py
Lo que gestiona los perfiles de jugadores con un json y funciones para actualizar y obtener los datos.
### Visuals.py
Un simple fichero donde se guardan las constantes de los títulos en ASCII para llamarlos luego en el GameManager y no ensuciarlo

## 🛠 Instalación 🛠
# Clonar el repositorio
```bash
git clone https://github.com/ItsazainBilbao/2503_dsft_Hundir_La_FLota_Itsazain.git
```
# Instalar dependencias
```bash
pip install playsound
pip install rich
```
## ▶️ Uso ▶️
# Ejecutar el juego
```bash
python main.py
```
