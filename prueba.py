import json
import heapq
from clases.Rutas import Rutas
from clases.Vehiculo import Vehiculo


# Cargar los datos del JSON
with open('matriz/matrizEjemplo2.json', 'r') as file:
    datos = json.load(file)

# Obtener la matriz del mapa
mapa = datos["mapa"]

vehiculo = Vehiculo(id=1, eficiencia_combustible=15)


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

"""
rutaMapa = Rutas(mapa, inicio, destino, vehiculo)
camino_encontrado = rutaMapa.astar(True)
camino_encontrado2 = rutaMapa.astar(False)



for reporte in vehiculo.reportes:
    reporte.getReporte()
    print("--------------------")



"""
1. Tiempo
2. Cll - carr
3. Algoritmo todas las rutas posibles
4. algoritmo 4
"""
