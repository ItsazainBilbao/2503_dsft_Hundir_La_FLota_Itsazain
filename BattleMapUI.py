from Board import Board
from rich.console import Console
from rich.table import Table
from rich import box
import numpy
import copy

class BattleMapUI:

    def __init__(self):
        pass

    def imprimirTablero(self, tablero : Board, nombre_jugador : str = ""):  
             
        tablilla = numpy.array(copy.deepcopy(tablero.tablero), dtype="object") 
        table = Table(title= str("Tablero de " + nombre_jugador), show_lines= True, box=box.DOUBLE, safe_box=True)        
        #Modifica valores de la copia de la tabla para imprimirlo fancy
        for i in range(len(tablilla)):
            for j in range(len(tablilla)):                
                if(tablilla[i][j] == tablero.CONST_SHIP):
                    tablilla[i][j] = "[yellow]1[/yellow]"
                elif(tablilla[i][j] == tablero.CONST_IMPACTED_WATER):                    
                    tablilla[i][j] = "[red]0[/red]"
                elif(tablilla[i][j] == tablero.CONST_IMPACTED_SHIP):                    
                    tablilla[i][j] = "[red]X[/red]"
                
                    
                    
        #Añade las columnas de la primera fila
        for i in range(len(tablilla)):     
            table.add_column( str(i+1), style="blue", justify= "center")
        #Añade la columna final 
        table.add_column("")
        #Añade el valor de cada fila de toda la tabla como fila a la tabla del rich
        #Al final añade letras mayórculas        
        for j in range(len(tablilla)):                
            table.add_row(*tablilla[j], chr(65+j))
        
        #Imprime por consola la tabla
        console = Console()
        console.print(table)
        pass