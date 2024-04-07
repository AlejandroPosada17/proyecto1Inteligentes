import json
import heapq
from clases.Rutas import Rutas


# Cargar los datos del JSON
with open('matriz/matrizEjemplo2.json', 'r') as file:
    datos = json.load(file)

# Obtener la matriz del mapa
mapa = datos["mapa"]


inicio = (0, 0)
destino = (2, 1)

"""
# RUTA 1 Y 2
rutaMapa = Rutas(mapa, inicio, destino)
camino_encontrado = rutaMapa.astar(True)

if camino_encontrado:
    print("Camino encontrado:", camino_encontrado)
else:
    print("No se encontró un camino.")
"""

#RUTA TUR
tourTrip = [(i, j) for i, fila in enumerate(mapa) for j, elemento in enumerate(fila) if elemento[2]]

caminoTourTrip =[]

rutaMapa = Rutas(mapa, (0,0), tourTrip[0])
caminoTourTrip = rutaMapa.astar(False)

for puntoInteres in tourTrip[1:]:
    rutaMapa = Rutas(mapa, caminoTourTrip[-1], puntoInteres)
    camino_encontrado = rutaMapa.astar(False)
    del camino_encontrado[0]
    caminoTourTrip.extend(camino_encontrado)

print("Ruta tourTrip: ",caminoTourTrip)
