import heapq
from collections import deque
from clases.nodoAestrella import Nodo
from clases.Vehiculo import Vehiculo
from clases.Reporte import Reporte


class Rutas:

    movimientos = [(-1,0),(1,0),(0,-1),(0,1)] # arriba - abajo - izquierda - derecha
    interaccion_adyacencia = {1: 0, 0: 1, 2: 3, 3: 2}

    def __init__(self, L, inicio, final, vehiculo:Vehiculo):
        self.L = L
        self.inicio = inicio
        self.final = final
        self.vehiculo = vehiculo
        self.id = f"Ruta {self.vehiculo.id}"
        self.distancia = 0
    
    def movimientos_posibles(self,nodo):
        candidatos = []
        for m in self.movimientos:
            candidatos.append((nodo.x+m[0],nodo.y+m[1]))
        return candidatos
        
    def heuristica(self, nodo:Nodo, destino:Nodo):         

        
    
        return abs(nodo.x - destino.x) + abs(nodo.y - destino.y)

    def es_valido(self, x,y):
        return 0 <= x < len(self.L) and 0 <= y < len(self.L[0])

    def es_viable(self,x,y):
        return self.L[x][y][0] == 0

    def astar(self, semaforizacion):
        
        lst_abiertos = []
        lst_cerrados = set()
        #Se crea con clase nodo, el nodo inicio y nodo final
        nodo_inicio = Nodo(self.inicio[0], self.inicio[1]) 
        nodo_destino = Nodo(self.final[0], self.final[1])

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

                
                ruta = camino[::-1]
                self.distancia = len(ruta)
                cantidad_calles = self.distancia
                cantidad_carreras = self.distancia
                tiempo = sum(self.L[x][y][1] for x, y in ruta if self.L[x][y][1])
                reporte = Reporte(self.vehiculo.costo_total *self.distancia,cantidad_carreras,cantidad_calles,tiempo)
                self.vehiculo.reportes.append(reporte)

                self.vehiculo.reportar_viaje(self.distancia / self.vehiculo.eficiencia_combustible, cantidad_calles, cantidad_carreras, tiempo)
                    
                return camino[::-1]
            
            candidatos = self.movimientos_posibles(nodo_actual)

            direccion_posible_movimiento = 0; #empieza hacia arriba
            for c in candidatos:
                
                #Si nodo actual puede salir en "direccion_posible_movimiento"
                if self.L[nodo_actual.x][nodo_actual.y][3][direccion_posible_movimiento] in ["dobleVia", "sale"]:
                    
                    adyacencias_nodo_candidato = self.interaccion_adyacencia.get(direccion_posible_movimiento)
                    x, y = c

                    #Si al nodo candidato se puede entrar por "adyacencias_nodo_candidato"
                    if self.L[x][y][3][adyacencias_nodo_candidato] in ["dobleVia", "entra"]:

                        if self.es_valido(x,y) and self.es_viable(x,y) and (x, y) not in lst_cerrados:

                            if semaforizacion:
                                valor_semaforo = 0
                                if self.L[x][y][1] == False:
                                    valor_semaforo = 0
                                else:
                                    valor_semaforo = self.L[x][y][1]

                                # Modificar el cálculo del costo del movimiento para incluir el costo del semáforo
                                costo_movimiento = nodo_actual.g + 1 + valor_semaforo  # 1 es el costo base del movimiento
                                nodo_candidato = Nodo(x, y, nodo_actual, valor_semaforo)  # Pasar el costo del semáforo como parámetro
                                nodo_candidato.g = costo_movimiento
                            else:
                                nodo_candidato = Nodo(x, y, nodo_actual)
                                nodo_candidato.g = nodo_actual.g + 1

                            #Distancia a destino sin ir diagonalmente
                            nodo_candidato.h = self.heuristica(nodo_candidato, nodo_destino)
                            nodo_candidato.f = nodo_candidato.g + nodo_candidato.h
                            heapq.heappush(lst_abiertos, nodo_candidato)
                            lst_cerrados.add((x, y))

                direccion_posible_movimiento += 1 
        
        return None


    def ruta_menor_consumo(self):
        lst_abiertos = []
        lst_cerrados = set()
        nodo_inicio = Nodo(self.inicio[0], self.inicio[1])
        nodo_destino = Nodo(self.final[0], self.final[1])

        heapq.heappush(lst_abiertos, nodo_inicio)

        while lst_abiertos:
            nodo_actual = heapq.heappop(lst_abiertos)
            lst_cerrados.add((nodo_actual.x, nodo_actual.y))

            if nodo_actual.x == nodo_destino.x and nodo_actual.y == nodo_destino.y:
                camino = []
                while nodo_actual:
                    camino.append((nodo_actual.x, nodo_actual.y))
                    nodo_actual = nodo_actual.padre
                ruta = camino[::-1]
                self.distancia = len(ruta)
                cantidad_calles = self.distancia
                cantidad_carreras = self.distancia
                tiempo = sum(self.L[x][y][1] for x, y in ruta if self.L[x][y][1])
                self.vehiculo.reportar_viaje(self.distancia / self.vehiculo.eficiencia_combustible, cantidad_calles, cantidad_carreras, tiempo)
                return ruta

            candidatos = self.movimientos_posibles(nodo_actual)

            direccion_posible_movimiento = 0
            for c in candidatos:
                if self.L[nodo_actual.x][nodo_actual.y][3][direccion_posible_movimiento] in ["dobleVia", "sale"]:
                    adyacencias_nodo_candidato = self.interaccion_adyacencia.get(direccion_posible_movimiento)
                    x, y = c

                    if self.L[x][y][3][adyacencias_nodo_candidato] in ["dobleVia", "entra"]:
                        if self.es_valido(x, y) and self.es_viable(x, y) and (x, y) not in lst_cerrados:

                            nodo_candidato = Nodo(x, y, nodo_actual)
                            nodo_candidato.g = nodo_actual.g + 1 / self.vehiculo.eficiencia_combustible

                            nodo_candidato.h = self.heuristica(nodo_candidato, nodo_destino)
                            nodo_candidato.f = nodo_candidato.g + nodo_candidato.h
                            heapq.heappush(lst_abiertos, nodo_candidato)
                            lst_cerrados.add((x, y))

                direccion_posible_movimiento += 1

        return None

