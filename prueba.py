import json
import heapq


# Cargar los datos del JSON
with open('matrizEjemplo2.json', 'r') as file:
    datos = json.load(file)

# Obtener la matriz del mapa
mapa = datos["mapa"]

# Función para procesar las adyacencias
def procesar_adyacencias(adyacencias):
    adyacencias_procesadas = []
    for adyacencia in adyacencias:
        if adyacencia == "dobleVia":
            adyacencias_procesadas.append(True)
        elif adyacencia == "entra":
            adyacencias_procesadas.append(1)
        elif adyacencia == "sale":
            adyacencias_procesadas.append(2)
        else:
            adyacencias_procesadas.append(False)
    return adyacencias_procesadas

# Crear la matriz
matriz = []
for fila in mapa:
    fila_matriz = []
    for elemento in fila:
        transitable, semaforo, punto_interes, adyacencias = elemento
        adyacencias_procesadas = procesar_adyacencias(adyacencias)
        fila_matriz.append(transitable)
    matriz.append(fila_matriz)

# Imprimir la matriz resultante
#for fila in matriz:
    #print(fila)

    

 
#print(mapa[1][0][1])
    

movimientos = [(-1,0),(1,0),(0,-1),(0,1)] # arriba - abajo - izquierda - derecha

interaccion_adyacencia = {1: 0, 0: 1, 2: 3, 3: 2}

class Nodo:
    def __init__(self, x, y, padre=None):
        self.x = x
        self.y = y
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0
    
    #con esto indicamos como quieremos que se comparen los objetos nodos. En este caso se compararan con el atributo F
    def __lt__(self, otro):
        return self.f < otro.f
    
def movimientos_posibles(nodo):
    candidatos = []
    for m in movimientos:
        candidatos.append((nodo.x+m[0],nodo.y+m[1]))
    return candidatos
    
def heuristica(nodo, destino):
    return abs(nodo.x - destino.x) + abs(nodo.y - destino.y)

def es_valido(L,x,y):
    return 0 <= x < len(L) and 0 <= y < len(L[0])

def es_viable(L,x,y):
    return L[x][y][0] == 0

def astar(L, inicio, final):
    filas, columnas = len(L), len(L[0])
    lst_abiertos = []
    lst_cerrados = set()
    #Se crea con clase nodo, el nodo inicio y nodo final
    nodo_inicio = Nodo(inicio[0], inicio[1]) 
    nodo_destino = Nodo(final[0], final[1])

    #Agregamos al heapq(lst_abiertos) el nodo nodo_inicio
    heapq.heappush(lst_abiertos, nodo_inicio)
    
    while lst_abiertos:

        #busca monticulo minimo y lo elimina. Luego agrega su posicion a lst_cerrados
        nodo_actual = heapq.heappop(lst_abiertos)
        lst_cerrados.add((nodo_actual.x, nodo_actual.y))
        
        if nodo_actual.x == nodo_destino.x and nodo_actual.y == nodo_destino.y:
            camino = []
            while nodo_actual:
                camino.append((nodo_actual.x, nodo_actual.y))
                nodo_actual = nodo_actual.padre
                
            return camino[::-1]
        
        candidatos = movimientos_posibles(nodo_actual)

        direccion_posible_movimiento = 0; #empieza hacia arriba
        for c in candidatos:
            
            #Si nodo actual puede salir en "direccion_posible_movimiento"
            if mapa[nodo_actual.x][nodo_actual.y][3][direccion_posible_movimiento] in ["dobleVia", "sale"]:
                
                adyacencias_nodo_candidato = interaccion_adyacencia.get(direccion_posible_movimiento)
                x, y = c

                #Si al nodo candidato se puede entrar por "adyacencias_nodo_candidato"
                if mapa[x][y][3][adyacencias_nodo_candidato] in ["dobleVia", "entra"]:

                    if es_valido(L,x,y) and es_viable(L,x,y) and (x, y) not in lst_cerrados:
                        nodo_candidato = Nodo(x, y, nodo_actual)
                        nodo_candidato.g = nodo_actual.g + 1

                        #Distancia a destino sin ir diagonalmente
                        nodo_candidato.h = heuristica(nodo_candidato, nodo_destino)
                        nodo_candidato.f = nodo_candidato.g + nodo_candidato.h
                        heapq.heappush(lst_abiertos, nodo_candidato)
                        lst_cerrados.add((x, y))

            direccion_posible_movimiento += 1 
    
    return None

inicio = (0, 0)
destino = (3, 3)
camino = astar(mapa, inicio, destino)
if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")

