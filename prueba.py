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

rutaMapa = Rutas(mapa, inicio, destino)

camino_encontrado = rutaMapa.astar(True)

if camino_encontrado:
    print("Camino encontrado:", camino_encontrado)
else:
    print("No se encontró un camino.")

