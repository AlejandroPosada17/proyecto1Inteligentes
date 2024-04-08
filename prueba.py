import json
from clases.Rutas import Rutas
from clases.Vehiculo import Vehiculo
import math


# Cargar los datos del JSON
with open('matriz/matrizEjemplo2.json', 'r') as file:
    datos = json.load(file)

# Obtener la matriz del mapa
mapa = datos["mapa"]

vehiculo1 = Vehiculo(id=1, eficiencia_combustible=15, x=0, y=0)
vehiculo2 = Vehiculo(id=2, eficiencia_combustible=15, x=3, y=3)

lista_vehiculos = [vehiculo1, vehiculo2]
tourTrip = [(i, j) for i, fila in enumerate(mapa) for j, elemento in enumerate(fila) if elemento[2]]

inicio = (0, 0)
destino = (2,1)

tipoRuta = 3

def distancia_puntos(punto1, punto2):
    return math.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)



distancia = -1
vehiculoSeleccionado = vehiculo1
for vehiculo in lista_vehiculos:
    distanciaTaxiPasajero = distancia_puntos((vehiculo.x,vehiculo.y),(inicio))
    if(distancia > distanciaTaxiPasajero):
        distancia = distanciaTaxiPasajero
        vehiculoSeleccionado = vehiculo


rutaMapa = Rutas(mapa, inicio, destino, vehiculoSeleccionado)
camino_encontrado =[]
if tipoRuta == 1:
    camino_encontrado = rutaMapa.astar(False)
elif tipoRuta == 2:
    camino_encontrado = rutaMapa.astar(True)
elif tipoRuta == 3:
    camino_encontrado = rutaMapa.ruta_menor_consumo()
elif tipoRuta == 5:
    #RUTA TUR
    caminoTourTrip =[]

    rutaMapa = Rutas(mapa, (0,0), tourTrip[0])
    caminoTourTrip = rutaMapa.astar(False)

    for puntoInteres in tourTrip[1:]:
        rutaMapa = Rutas(mapa, caminoTourTrip[-1], puntoInteres)
        camino_encontrado = rutaMapa.astar(False)
        del camino_encontrado[0]
        caminoTourTrip.extend(camino_encontrado)

    print("Ruta tourTrip: ",caminoTourTrip)




print("----VEHICULO 1----------------")

for reporte in vehiculo1.reportes:
    reporte.getReporte()
    print("--------------------")
print("----VEHICULO 2----------------")
for reporte in vehiculo2.reportes:
    reporte.getReporte()
    print("--------------------")


print("CAMINO ENCONTRADO: ")
print(camino_encontrado)

"""

1. Tiempo
2. Cll - carr


5. algoritmo 4

"""
